export default function Sidebar() {
  return (
    <nav className="hidden md:flex flex-col justify-between py-stack-lg bg-[#ffffff0d] backdrop-blur-xl fixed left-0 top-0 h-full w-[280px] border-r border-[#ffffff1a] shadow-[0_0_20px_rgba(226,55,68,0.1)] z-40 transition-transform duration-300">
      <div className="px-container-padding-desktop">
        <div className="flex items-center gap-3 mb-stack-lg">
          <div className="w-10 h-10 rounded-full bg-surface-container-high flex items-center justify-center overflow-hidden border border-outline/20">
            <span className="material-symbols-outlined text-primary">restaurant</span>
          </div>
          <div>
            <h1 className="font-display-lg text-display-lg font-bold text-primary text-xl leading-tight">Lumiere AI</h1>
            <p className="font-label-caps text-label-caps text-on-surface-variant">Premium Concierge</p>
          </div>
        </div>
        <ul className="space-y-unit">
          <li>
            <a className="flex items-center gap-3 text-on-surface font-bold border-l-4 border-primary pl-4 py-3 bg-[#ffffff0a] rounded-r-lg font-interactive-label text-interactive-label" href="#">
              <span className="material-symbols-outlined" style={{ fontVariationSettings: "'FILL' 1" }}>recommend</span>
              Recommendations
            </a>
          </li>
          <li>
            <a className="flex items-center gap-3 text-on-surface-variant pl-4 py-3 hover:text-on-surface hover:bg-[#ffffff14] transition-colors duration-300 rounded-r-lg font-interactive-label text-interactive-label" href="#">
              <span className="material-symbols-outlined">settings</span>
              Settings
            </a>
          </li>
        </ul>
        
        {/* We removed the Groq API key input since it's strictly server-side now! */}
      </div>
      <div className="px-container-padding-desktop">
        <p className="font-label-caps text-label-caps text-on-surface-variant mb-2">Powered By</p>
        <ul className="space-y-2 opacity-70">
          <li className="flex items-center gap-2 text-sm text-on-surface">
            <span className="material-symbols-outlined text-[16px]">database</span> Data: Zomato
          </li>
          <li className="flex items-center gap-2 text-sm text-on-surface">
            <span className="material-symbols-outlined text-[16px]">neurology</span> HuggingFace
          </li>
        </ul>
      </div>
    </nav>
  );
}
