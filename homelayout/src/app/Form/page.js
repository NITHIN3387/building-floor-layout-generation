"use client";
import { useState } from "react";

export default function FormPage() {
  const [formData, setFormData] = useState({
    doorFacing: "",
    rooms: [],
  });

  const [output, setOutput] = useState(null);

  const handleChange = (e) => {
    const { id, name, value } = e.target;

    if (id === "rooms") {
      setFormData((prev) => ({
        ...prev,
        rooms: { ...prev.rooms, [name]: value },
      }));
    } else {
      setFormData((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setOutput("loading");

    const response = await fetch("http://localhost:5000/generate-layout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formData),
    });

    await response.json().then((data) => {
      const image = data.file_name;
      const dimenstions = data.room_dimensions;

      setOutput({ image, dimenstions });
    });
  };

  return (
    <div className="flex flex-col md:flex-row items-center min-h-screen bg-white p-8 space-y-8 md:space-y-0 md:space-x-8">
      {/* Form Section */}
      <img className="absolute w-40 h-40 right-8 top-8" src="/compass.webp" />
      <div className="flex flex-col items-center md:w-1/2">
        <h1 className="text-2xl font-bold text-black mb-8">
          Fill Your Requirements
        </h1>
        <form
          className="w-full max-w-md text-black space-y-6"
          onSubmit={(e) => handleSubmit(e)}
        >
          <div>
            <label className="block font-semibold mb-1">Door Facing</label>
            <select
              name="doorFacing"
              value={formData.doorFacing}
              onChange={handleChange}
              className="w-full border rounded-lg p-2"
            >
              <option value="">Select Direction</option>
              <option value="North">North</option>
              <option value="North East">North East</option>
              <option value="East">East</option>
            </select>
          </div>
          <div>
            <label className="block font-semibold mb-1">
              Total Area Length (in feet)
            </label>
            <input
              type="number"
              name="totalLength"
              onChange={handleChange}
              className="w-full border rounded-lg p-2"
              placeholder="Enter total length"
              min="1"
            />
          </div>
          <div>
            <label className="block font-semibold mb-1">
              Total Area width (in feet)
            </label>
            <input
              type="number"
              name="totalWidth"
              onChange={handleChange}
              className="w-full border rounded-lg p-2"
              placeholder="Enter total width"
              min="1"
            />
          </div>
          <div>
            <label className="block font-semibold mb-1">Rooms Required:</label>
            <div className="space-y-2">
              {[
                ["Living Room", "#eee8aa"],
                ["Bedroom", "#faa430"],
                ["Dining Room", "#db71d6"],
                ["Kitchen", "#f08080"],
                ["Bathroom", "#add8e6"],
                ["Balcony", "#6a8e22"],
              ].map((room) => (
                <label key={room} className="grid grid-cols-[1fr_1fr_auto] items-center gap-4">
                  <p className="whitespace-nowrap">{room[0]}</p>
                  <input
                    type="number"
                    id="rooms"
                    name={room[0]}
                    defaultValue={0}
                    onChange={handleChange}
                    className="w-full border rounded-lg p-2"
                  />
                  <div className="w-10 h-10 rounded-lg" style={{ backgroundColor: room[1] }} />
                </label>
              ))}
            </div>
          </div>
          <button
            type="submit"
            className="w-full mt-4 bg-purple-900 text-white py-2 rounded-lg shadow-lg hover:bg-purple-800"
            disabled={output === "loading"}
          >
            Generate
          </button>
        </form>
      </div>

      {/* Output Section */}
      {output &&
        (output === "loading" ? (
          <div className="flex flex-col items-center md:w-1/2 space-y-4">
            <h2 className="text-xl font-bold text-black">Generated Image</h2>
            <div className="flex items-center gap-4">
              <div className="h-72 w-72 animate-pulse bg-slate-200 rounded-lg" />
              <div className="h-72 w-72 animate-pulse bg-slate-200 rounded-lg" />
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center md:w-1/2 space-y-4">
            <h2 className="text-xl font-bold text-black">Generated Image</h2>
            <div className="flex items-center">
              <img
                src={output.image}
                alt="Generated Layout"
                className="w-full max-w-md rounded-lg"
              />
              <div className="m-5 text-black">
                <h2>Room Dimensions</h2>
                <table className="w-full border-collapse text-left mt-2.5">
                  <thead>
                    <tr className="bg-purple-900 text-white">
                      <th className="border border-slate-300 p-2">Room</th>
                      <th className="border border-slate-300 p-2">
                        Dimensions (Length x Width)
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.entries(output.dimenstions).map(
                      ([room, [length, breadth]]) => (
                        <tr key={room}>
                          <td className="border border-slate-300 p-2">
                            {room}
                          </td>
                          <td className="border border-slate-300 p-2">
                            {length.toFixed(2)} x {breadth.toFixed(2)} ft
                          </td>
                        </tr>
                      )
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        ))}
    </div>
  );
}
