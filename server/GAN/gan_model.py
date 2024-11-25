import tensorflow as tf
import tensorflow_hub as hub

from tensorflow.keras.layers import Input, Dense, Flatten, Conv2D, Conv2DTranspose, LeakyReLU, Reshape, Concatenate, BatchNormalization, Dropout
from tensorflow.keras.models import Model

import matplotlib.pyplot as plt
import networkx as nx

import os
import uuid

# physical_devices = tf.config.list_physical_devices('GPU')

# if len(physical_devices) > 0:
#     print(f"TensorFlow is using {len(physical_devices)} GPU(s).")
# else:
#     print("No GPU available.")

def generate(direction, rooms, length, width):
  PRE_TRAINED_MODELS_PATH = '/media/nithin/DATA/final-project/AI-Driven-Building-Floor-Layout-Generation-System/server/GAN/saved-models'

  IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS = 128, 128, 3

  NOISE_DIM = 100
  EMBEDDING_DIM = 512

  def get_caption_embeddings(captions):
    embed = hub.load("https://www.kaggle.com/models/google/universal-sentence-encoder/TensorFlow2/universal-sentence-encoder/2")
    return embed(captions)

  def build_generator():
      # Inputs
      noise = Input(shape=(NOISE_DIM,))
      caption_embedding = Input(shape=(EMBEDDING_DIM,))

      # Combine noise and caption embedding
      combined_input = Concatenate()([noise, caption_embedding])
      
      # Upscale to starting dimensions
      x = Dense(16 * 16 * 256, use_bias=False)(combined_input)
      x = BatchNormalization()(x)
      x = LeakyReLU()(x)
      x = Reshape((16, 16, 256))(x)

      # Upsampling to reach 128x128
      x = Conv2DTranspose(128, (4, 4), strides=(2, 2), padding='same', use_bias=False)(x)
      x = BatchNormalization()(x)
      x = LeakyReLU()(x)

      x = Conv2DTranspose(64, (4, 4), strides=(2, 2), padding='same', use_bias=False)(x)
      x = BatchNormalization()(x)
      x = LeakyReLU()(x)

      x = Conv2DTranspose(32, (4, 4), strides=(2, 2), padding='same', use_bias=False)(x)
      x = BatchNormalization()(x)
      x = LeakyReLU()(x)

      # Final layer to match image shape
      output_img = Conv2DTranspose(IMG_CHANNELS, (4, 4), strides=(1, 1), padding="same", use_bias=False, activation="tanh")(x)

      # Define model
      generator = Model([noise, caption_embedding], output_img, name="Generator")
      return generator

  generator = build_generator()

#   def build_discriminator():
#       # Image input
#       img_input = Input(shape=(IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS))
#       caption_embedding = Input(shape=(EMBEDDING_DIM,))

#       # Process image
#       x = Conv2D(64, (4, 4), strides=(2, 2), padding='same')(img_input)
#       x = LeakyReLU()(x)
#       x = Dropout(0.3)(x)

#       x = Conv2D(128, (4, 4), strides=(2, 2), padding='same')(x)
#       x = BatchNormalization()(x)
#       x = LeakyReLU()(x)
#       x = Dropout(0.3)(x)

#       x = Conv2D(256, (4, 4), strides=(2, 2), padding='same')(x)
#       x = BatchNormalization()(x)
#       x = LeakyReLU()(x)
#       x = Dropout(0.3)(x)

#       x = Flatten()(x)
#       x = Dense(512)(x)
#       x = LeakyReLU()(x)

#       # Combine image and caption embedding
#       combined = Concatenate()([x, caption_embedding])
#       combined = Dense(512)(combined)
#       combined = LeakyReLU()(combined)
#       combined = Flatten()(combined)
      
#       # Output layer
#       output = Dense(1, activation="sigmoid")(combined)

#       # Define model
#       discriminator = Model([img_input, caption_embedding], output, name="Discriminator")
#       return discriminator

  # Build and summarize the model
#   discriminator = build_discriminator()

  # Room details: aspect ratios for dimension calculation
  room_aspect_ratios = {
      'living_room': 4 / 3,
      'bedroom': 3 / 2,
      'dining_room': 4 / 3,
      'kitchen': 4 / 3,
      'bathroom': 2 / 1,
      'toilet': 2 / 1,
  }

  # Function to calculate room sizes
  def calculate_room_sizes(total_area, rooms):
      total_rooms = sum(rooms.values())
      room_sizes = {room: (count / total_rooms) * total_area for room, count in rooms.items()}
      return room_sizes

  # Function to calculate room dimensions (length and breadth)
  def calculate_length_breadth(area, aspect_ratio):
      length = (area * aspect_ratio) ** 0.5
      breadth = area / length
      return length, breadth

  # Function to generate descriptive captions based on layout and room dimensions
  def generate_caption(graph, direction, room_dimensions):
      caption = f"The main door of the house faces {direction}. "

      descriptions = []
      for node, data in graph.nodes(data=True):
          room_name = data['name']
          if room_name in room_dimensions:
              length, breadth = room_dimensions[room_name]
              square_footage = length * breadth
              neighbors = list(graph.neighbors(node))
              
              # Identify neighbor directions
              connections = []
              for neighbor in neighbors:
                  neighbor_data = graph[node][neighbor]
                  direction = neighbor_data.get('direction', 'adjacent')  # Use direction if available
                  connections.append(f"{graph.nodes[neighbor]['name'].replace('_', ' ')} to the {direction}")

              if connections:
                  connection_desc = ", ".join(connections)
                  room_description = (
                      f"The {room_name.replace('_', ' ')} is approximately {length:.2f} feet wide by {breadth:.2f} feet deep, "
                      f"for a total square footage of {square_footage:.2f}. It has {connection_desc}."
                  )
              else:
                  room_description = (
                      f"The {room_name.replace('_', ' ')} is approximately {length:.2f} feet wide by {breadth:.2f} feet deep, "
                      f"for a total square footage of {square_footage:.2f}. It stands independently."
                  )
              descriptions.append(room_description)

      caption += " ".join(descriptions)
      return caption.strip()

  # Create layout graph
  def create_graph(rooms):
      G = nx.Graph()
      node_id = 1
      directions = ["north", "east", "south", "west"]  # Example directions
      for room, count in rooms.items():
          for _ in range(count):
              G.add_node(node_id, name=room)
              if node_id > 1:
                  G.add_edge(node_id - 1, node_id, direction=directions[(node_id - 2) % 4])  # Cycle through directions
              node_id += 1
      return G
  total_area = length * width

  # Calculate room sizes and dimensions
  room_sizes = calculate_room_sizes(total_area, rooms)
  room_dimensions = {
      room: calculate_length_breadth(area, room_aspect_ratios.get(room, 1))
      for room, area in room_sizes.items()
  }

  # Fixed inputs and layout caption generation
  def generate_layout_caption():
      # Create layout graph
      layout_graph = create_graph(rooms)

      # Generate caption
      caption = generate_caption(layout_graph, direction, room_dimensions)
      return caption


  caption = [generate_layout_caption()]

  generator.load_weights(f'{PRE_TRAINED_MODELS_PATH}/generators/generator_epoch_420.h5')
#   discriminator.load_weights(f'{PRE_TRAINED_MODELS_PATH}/discriminators/discriminator_epoch_240.h5')

  noise = tf.random.normal([1, NOISE_DIM])
  caption_embeddings = get_caption_embeddings(caption)

  def save_generated_image(generated_image):
      base_dir = os.path.dirname(os.path.abspath(__file__))  # Current script's directory
      save_dir = os.path.join(base_dir, "../../homelayout/public/generated_images")
    
      os.makedirs(save_dir, exist_ok=True)
      
      # Save the image
      filename = uuid.uuid4().hex
      file_path = os.path.join(save_dir, f"{filename}.png")
      plt.figure(figsize=(5, 5))
      plt.imshow(generated_image[0, :, :, :])
      plt.axis("off")
      plt.plot()
      plt.savefig(file_path)
      return f"/generated_images/{filename}.png"

  generated_image = generator([noise, caption_embeddings], training=False)

  file_path = save_generated_image(generated_image)
  return file_path, room_dimensions


