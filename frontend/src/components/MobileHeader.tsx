export default function MobileHeader() {
  return (
    <header className="md:hidden docked full-width top-0 z-50 bg-surface/80 backdrop-blur-md border-b border-outline-variant/20 shadow-sm flex justify-between items-center px-container-padding-mobile py-4 fixed w-full">
      <h1 className="font-display-lg-mobile text-display-lg-mobile tracking-tight text-primary text-2xl">Lumiere AI</h1>
      <button className="text-on-surface-variant p-2">
        <span className="material-symbols-outlined">menu</span>
      </button>
    </header>
  );
}
