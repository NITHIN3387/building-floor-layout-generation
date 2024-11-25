import Link from 'next/link';

export default function Home() {
  return (
    <div className="flex items-center justify-center h-screen bg-black text-gold">
      <div className="text-center">
        {/* Logo and Title */}
        <div className="relative mb-8">
          <img
            src="/a3.jpg"
            alt="Placeholder Logo"
            className="w-50 h-44 mx-auto"
          />
          <h1 className="text-5xl font-serif text-yellow-500 mt-4">Layout Loom</h1>
        </div>

        {/* Description */}
        <p className="mt-6 text-lg text-white max-w-md mx-auto leading-relaxed">
          Layout Loom suggests a platform or service dedicated to crafting
          detailed and artistic home designs, where every layout is thoughtfully
          created like a masterpiece woven on a loom.
        </p>

        {/* Button */}
        <Link href="./Form/">
          <button className="mt-8 px-6 py-3 bg-yellow-500 text-black rounded-md shadow-lg text-lg hover:bg-yellow-700">
            Get Started
          </button>
        </Link>
      </div>

      {/* Decorative Icons */}
      <div className="absolute top-10 right-10">
        <img
          src="/a1.jpg"
          alt="Decorative Icon 1"
          className="w-80 h-76"
        />
      </div>
      <div className="absolute bottom-10 left-10">
        <img
          src="/a2.jpg"
          alt="Decorative Icon 2"
          className="w-80 h-76"
        />
      </div>
    </div>
  );
}
