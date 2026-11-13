from pathlib import Path

target = Path("EditAI/frontend/src/components/Navbar.jsx")
text = target.read_text(encoding="utf-8")

# 1. Update component props
old_props = """export default function Navbar({
  projectName,
  onSaveProject,
  onNewProject,
  onOpenProjectList,
  onAnalyze,
  isAnalyzing,
  onOpenExport,
  onOpenAssemblyStage,
  onLoadSample,
  hasMedia,
  activeRightTab,
  setActiveRightTab,
  isEdited
}) {"""

new_props = """export default function Navbar({
  projectName,
  onSaveProject,
  onNewProject,
  onOpenProjectList,
  onAnalyze,
  isAnalyzing,
  onOpenExport,
  onOpenAssemblyStage,
  onLoadSample,
  onOpenFolder,
  hasMedia,
  activeRightTab,
  setActiveRightTab,
  isAIAssistantOpen = true,
  onToggleAIAssistant,
  activeLeftTab = 'media',
  setActiveLeftTab,
  isEdited
}) {"""

assert old_props in text, "old_props not found in Navbar.jsx"
text = text.replace(old_props, new_props, 1)

# 2. Add Open Folder button in the top menu bar
old_sample_btn = """        {/* Quick Demo Sample Loader */}
        <div className="flex items-center gap-3 text-[11px]">
          <button
            onClick={onLoadSample}
            className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#1a1c20] hover:bg-[#25272e] text-[#b5b9c4] border border-[#2b2d35] transition"
            title="Load 30s Multi-Scene Demo Sample Assets"
          >
            <FolderOpen className="w-3 h-3 text-[#828692]" />
            <span>Load Demo Sample</span>
          </button>
        </div>"""

new_sample_btn = """        {/* Quick Demo & Local Folder Loaders */}
        <div className="flex items-center gap-2 text-[11px]">
          {onOpenFolder && (
            <button
              onClick={onOpenFolder}
              className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#181d26] hover:bg-[#222b3a] text-[#86a6d6] border border-[#2a3c54] transition"
              title="Connect and import all video clips from a computer directory"
            >
              <FolderOpen className="w-3 h-3 text-[#38bdf8]" />
              <span>Open Folder</span>
            </button>
          )}
          <button
            onClick={onLoadSample}
            className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#1a1c20] hover:bg-[#25272e] text-[#b5b9c4] border border-[#2b2d35] transition"
            title="Load 30s Multi-Scene Demo Sample Assets"
          >
            <Film className="w-3 h-3 text-[#828692]" />
            <span>Load Demo Sample</span>
          </button>
        </div>"""

assert old_sample_btn in text, "old_sample_btn not found in Navbar.jsx"
text = text.replace(old_sample_btn, new_sample_btn, 1)

# 3. Update Left tabs (Media Pool, Sync Bin, Transitions, Titles, Effects) with active state and onClick
old_left_tabs = """        {/* Left tabs: Media Pool, Sync Bin, Transitions, etc. */}
        <div className="flex items-center gap-1 text-[11px]">
          <button className="px-2.5 py-1 rounded bg-[#25272e] text-[#e0e3eb] font-medium border border-[#32353e]">
            Media Pool
          </button>
          <button className="px-2 py-1 rounded hover:bg-[#202227] text-[#868a96] hover:text-[#c4c7d0] transition">
            Sync Bin
          </button>
          <button className="px-2 py-1 rounded hover:bg-[#202227] text-[#868a96] hover:text-[#c4c7d0] transition">
            Transitions
          </button>
          <button className="px-2 py-1 rounded hover:bg-[#202227] text-[#868a96] hover:text-[#c4c7d0] transition">
            Titles
          </button>
          <button className="px-2 py-1 rounded hover:bg-[#202227] text-[#868a96] hover:text-[#c4c7d0] transition">
            Effects
          </button>
        </div>"""

new_left_tabs = """        {/* Left tabs: Media Pool, Sync Bin, Transitions, Titles, Effects */}
        <div className="flex items-center gap-1 text-[11px]">
          <button
            onClick={() => setActiveLeftTab && setActiveLeftTab('media')}
            className={`px-2.5 py-1 rounded font-medium transition border cursor-pointer ${
              activeLeftTab === 'media'
                ? 'bg-[#25272e] text-[#e0e3eb] border-[#32353e] shadow-xs'
                : 'bg-transparent text-[#868a96] hover:text-[#c4c7d0] border-transparent'
            }`}
            title="Media Pool (Master Assets & Imported Clips)"
          >
            Media Pool
          </button>
          <button
            onClick={() => setActiveLeftTab && setActiveLeftTab('sync_bin')}
            className={`px-2.5 py-1 rounded font-medium transition border cursor-pointer ${
              activeLeftTab === 'sync_bin'
                ? 'bg-[#202834] text-[#7ea5dc] border-[#344b68] shadow-xs'
                : 'bg-transparent text-[#868a96] hover:text-[#c4c7d0] border-transparent'
            }`}
            title="Sync Bin (Multi-Camera & Audio Waveform Synchronization)"
          >
            Sync Bin
          </button>
          <button
            onClick={() => setActiveLeftTab && setActiveLeftTab('transitions')}
            className={`px-2.5 py-1 rounded font-medium transition border cursor-pointer ${
              activeLeftTab === 'transitions'
                ? 'bg-[#2a261c] text-[#e6b360] border-[#4a3f28] shadow-xs'
                : 'bg-transparent text-[#868a96] hover:text-[#c4c7d0] border-transparent'
            }`}
            title="Video Transitions Library (Dissolves, Whip Pans, Glitch, Zooms)"
          >
            Transitions
          </button>
          <button
            onClick={() => setActiveLeftTab && setActiveLeftTab('titles')}
            className={`px-2.5 py-1 rounded font-medium transition border cursor-pointer ${
              activeLeftTab === 'titles'
                ? 'bg-[#1a2632] text-[#48b2e8] border-[#29425a] shadow-xs'
                : 'bg-transparent text-[#868a96] hover:text-[#c4c7d0] border-transparent'
            }`}
            title="Titles & Text Generator (Lower Thirds, Headlines, Captions)"
          >
            Titles
          </button>
          <button
            onClick={() => setActiveLeftTab && setActiveLeftTab('effects')}
            className={`px-2.5 py-1 rounded font-medium transition border cursor-pointer ${
              activeLeftTab === 'effects'
                ? 'bg-[#261c30] text-[#c084fc] border-[#46305a] shadow-xs'
                : 'bg-transparent text-[#868a96] hover:text-[#c4c7d0] border-transparent'
            }`}
            title="Effects & Color LUTs (Teal & Orange, Noir, Vintage Film, Audio FX)"
          >
            Effects
          </button>
        </div>"""

assert old_left_tabs in text, "old_left_tabs not found in Navbar.jsx"
text = text.replace(old_left_tabs, new_left_tabs, 1)

# 4. Update AI Assistant toggle button to behave like Copilot
old_assistant_btn = """          {/* AI Assistant Toggle */}
          <button
            onClick={() => setActiveRightTab('ai')}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded border transition ${
              activeRightTab === 'ai'
                ? 'bg-[#252830] text-[#e0e3eb] border-[#3e424e]'
                : 'bg-transparent text-[#7e828e] hover:text-[#c4c7d0] border-transparent'
            }`}
          >
            <Sparkles className="w-3 h-3 text-[#d48b3b]" />
            <span>AI Assistant</span>
          </button>"""

new_assistant_btn = """          {/* AI Assistant Copilot Toggle (Opens / Closes like Copilot) */}
          <button
            onClick={() => {
              if (onToggleAIAssistant) {
                onToggleAIAssistant();
              } else {
                setActiveRightTab(activeRightTab === 'ai' ? 'inspector' : 'ai');
              }
            }}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded border transition cursor-pointer ${
              isAIAssistantOpen && activeRightTab === 'ai'
                ? 'bg-[#202834] text-[#e0e3eb] border-[#445b78] shadow-sm ring-1 ring-[#5594df]/30'
                : 'bg-transparent text-[#7e828e] hover:text-[#c4c7d0] border-transparent'
            }`}
            title={isAIAssistantOpen && activeRightTab === 'ai' ? "Close AI Copilot Panel" : "Open AI Copilot Panel"}
          >
            <Sparkles className={`w-3 h-3 ${isAIAssistantOpen && activeRightTab === 'ai' ? 'text-[#38bdf8] animate-pulse' : 'text-[#d48b3b]'}`} />
            <span>AI Assistant</span>
            <span className={`text-[8px] font-mono px-1 py-0.2 rounded ${isAIAssistantOpen && activeRightTab === 'ai' ? 'bg-[#28384d] text-[#7ea5dc]' : 'bg-[#18191d] text-[#636875]'}`}>
              {isAIAssistantOpen && activeRightTab === 'ai' ? 'Open' : 'Copilot'}
            </span>
          </button>"""

assert old_assistant_btn in text, "old_assistant_btn not found in Navbar.jsx"
text = text.replace(old_assistant_btn, new_assistant_btn, 1)

target.write_text(text, encoding="utf-8")
print("Navbar.jsx patched successfully!")

