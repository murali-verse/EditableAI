import React from 'react';
import {
  Film,
  Download,
  FolderOpen,
  Save,
  Sliders,
  Sparkles,
  Maximize,
  Volume2,
  Layers,
  FileCode
} from 'lucide-react';

export default function Navbar({
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
}) {
  return (
    <div className="flex flex-col bg-[#121316] border-b border-[#24262b] select-none text-[12px] text-[#a0a4ae]">
      {/* 1. Main Application & File Menu Bar */}
      <div className="h-6 px-3 flex items-center justify-between border-b border-[#1c1d21] text-[11px] bg-[#0e0f11]">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5 font-semibold text-[#d0d3dc]">
            {/* Subtle DaVinci-inspired three-circle emblem */}
            <div className="flex items-center gap-0.5">
              <span className="w-1.5 h-1.5 rounded-full bg-[#c084fc]" />
              <span className="w-1.5 h-1.5 rounded-full bg-[#a855f7]" />
              <span className="w-1.5 h-1.5 rounded-full bg-[#7c3aed]" />
            </div>
            <span className="tracking-wide">REELCRAFT AI</span>
          </div>

          <div className="flex items-center gap-3 text-[#828692]">
            <span className="hover:text-white cursor-pointer" onClick={onNewProject}>File</span>
            <span className="hover:text-white cursor-pointer">Edit</span>
            <span className="hover:text-white cursor-pointer">Trim</span>
            <span className="hover:text-white cursor-pointer">Timeline</span>
            <span className="hover:text-white cursor-pointer">Clip</span>
            <span className="hover:text-white cursor-pointer">Mark</span>
            <span className="hover:text-white cursor-pointer">View</span>
            <span className="hover:text-white cursor-pointer">Playback</span>
            <span className="hover:text-white cursor-pointer">Fusion</span>
            <span className="hover:text-white cursor-pointer">Color</span>
            <span className="hover:text-white cursor-pointer">Fairlight</span>
            <span className="hover:text-white cursor-pointer">Help</span>
          </div>
        </div>

        {/* Quick Demo & Local Folder Loaders */}
        <div className="flex items-center gap-2 text-[11px]">
          {onOpenFolder && (
            <button
              onClick={onOpenFolder}
              className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#261c30] hover:bg-[#351e4c] text-[#c084fc] border border-[#7c3aed] transition"
              title="Connect and import all video clips from a computer directory"
            >
              <FolderOpen className="w-3 h-3 text-[#c084fc]" />
              <span>Open Folder</span>
            </button>
          )}
          <button
            onClick={onLoadSample}
            className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#1e1728] hover:bg-[#2c1d3c] text-[#c084fc] border border-[#482c66] hover:border-[#7c3aed] transition"
            title="Load 30s Multi-Scene Demo Sample Assets"
          >
            <Film className="w-3 h-3 text-[#c084fc]" />
            <span>Load Demo Sample</span>
          </button>
        </div>
      </div>

      {/* 2. DaVinci Resolve Secondary Tool Header */}
      <div className="h-9 px-3 flex items-center justify-between bg-[#16171b]">
        {/* Left tabs: Media Pool, Sync Bin, Transitions, Titles, Effects */}
        <div className="flex items-center gap-1 text-[11px]">
          <button
            onClick={() => setActiveLeftTab && setActiveLeftTab('media')}
            className={`px-2.5 py-1 rounded font-medium transition border cursor-pointer ${activeLeftTab === 'media'
                ? 'bg-[#261c30] text-[#c084fc] border-[#7c3aed] shadow-xs'
                : 'bg-transparent text-[#868a96] hover:text-[#c084fc] hover:bg-[#261c30]/40 border-transparent'
              }`}
            title="Media Pool (Master Assets & Imported Clips)"
          >
            Media Pool
          </button>
          <button
            onClick={() => setActiveLeftTab && setActiveLeftTab('sync_bin')}
            className={`px-2.5 py-1 rounded font-medium transition border cursor-pointer ${activeLeftTab === 'sync_bin'
                ? 'bg-[#261c30] text-[#c084fc] border-[#7c3aed] shadow-xs'
                : 'bg-transparent text-[#868a96] hover:text-[#c084fc] hover:bg-[#261c30]/40 border-transparent'
              }`}
            title="Sync Bin (Multi-Camera & Audio Waveform Synchronization)"
          >
            Sync Bin
          </button>
          <button
            onClick={() => setActiveLeftTab && setActiveLeftTab('transitions')}
            className={`px-2.5 py-1 rounded font-medium transition border cursor-pointer ${activeLeftTab === 'transitions'
                ? 'bg-[#261c30] text-[#c084fc] border-[#7c3aed] shadow-xs'
                : 'bg-transparent text-[#868a96] hover:text-[#c084fc] hover:bg-[#261c30]/40 border-transparent'
              }`}
            title="Video Transitions Library (Dissolves, Whip Pans, Glitch, Zooms)"
          >
            Transitions
          </button>
          <button
            onClick={() => setActiveLeftTab && setActiveLeftTab('titles')}
            className={`px-2.5 py-1 rounded font-medium transition border cursor-pointer ${activeLeftTab === 'titles'
                ? 'bg-[#261c30] text-[#c084fc] border-[#7c3aed] shadow-xs'
                : 'bg-transparent text-[#868a96] hover:text-[#c084fc] hover:bg-[#261c30]/40 border-transparent'
              }`}
            title="Titles & Text Generator (Lower Thirds, Headlines, Captions)"
          >
            Titles
          </button>
          <button
            onClick={() => setActiveLeftTab && setActiveLeftTab('effects')}
            className={`px-2.5 py-1 rounded font-medium transition border cursor-pointer ${activeLeftTab === 'effects'
                ? 'bg-[#261c30] text-[#c084fc] border-[#7c3aed] shadow-xs'
                : 'bg-transparent text-[#868a96] hover:text-[#c084fc] hover:bg-[#261c30]/40 border-transparent'
              }`}
            title="Effects & Color LUTs (Teal & Orange, Noir, Vintage Film, Audio FX)"
          >
            Effects
          </button>
        </div>

        {/* Center: Project title & Edit status */}
        <div className="flex items-center gap-2">
          <button
            onClick={onOpenProjectList}
            className="font-medium text-[#d8dbe4] hover:text-white text-xs flex items-center gap-1.5"
            title="Open or Switch Project"
          >
            <span>{projectName}</span>
          </button>
          {isEdited && (
            <span className="text-[10px] text-[#737785] tracking-wide uppercase px-1 py-0.2 rounded border border-[#2a2c33]">
              Edited
            </span>
          )}
          <button
            onClick={onSaveProject}
            className="p-1 rounded text-[#7e828e] hover:text-white hover:bg-[#22242a] transition ml-1"
            title="Save Project (Ctrl+S)"
          >
            <Save className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Right action toggles: AI Video Pipeline, Analyze, Quick Export, Inspector, AI Assistant */}
        <div className="flex items-center gap-1.5 text-[11px]">
          <button
            onClick={onOpenAssemblyStage}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#261c30] hover:bg-[#351e4c] text-[#c084fc] border border-[#7c3aed] transition shadow-xs cursor-pointer"
            title="Open AI Video Pipeline (Upload, Analysis, Global Story Planning, Validation, OTIO Export)"
          >
            <Sparkles className="w-3 h-3 text-[#c084fc]" />
            <span className="font-medium text-[#c084fc]">AI Video Pipeline</span>
          </button>

          <button
            onClick={onAnalyze}
            disabled={!hasMedia || isAnalyzing}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#1e1728] hover:bg-[#2c1d3c] text-[#c084fc] border border-[#482c66] hover:border-[#7c3aed] transition disabled:opacity-40 cursor-pointer"
            title="Analyze Video for Scenes, Silences, and Dialogue"
          >
            <Sparkles className={`w-3 h-3 text-[#b8bcc8] ${isAnalyzing ? 'animate-spin' : ''}`} />
            <span>{isAnalyzing ? 'Analyzing...' : 'Analyze'}</span>
          </button>

          <button
            onClick={onOpenExport}
            disabled={!hasMedia}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-[#1e1728] hover:bg-[#2c1d3c] text-[#c084fc] border border-[#482c66] hover:border-[#7c3aed] transition disabled:opacity-40 cursor-pointer"
            title="Render & Export Timeline as MP4"
          >
            <Download className="w-3 h-3 text-[#c084fc]" />
            <span>Quick Export</span>
          </button>

          <div className="w-px h-3.5 bg-[#2a2c33] mx-1" />

          {/* Inspector Toggle */}
          <button
            onClick={() => setActiveRightTab('inspector')}
            className={`flex items-center gap-1 px-2.5 py-1 rounded border transition ${activeRightTab === 'inspector'
                ? 'bg-[#261c30] text-[#c084fc] border-[#7c3aed] shadow-xs'
                : 'bg-transparent text-[#7e828e] hover:text-[#c084fc] hover:bg-[#261c30]/40 border-transparent'
              }`}
          >
            <Sliders className="w-3 h-3" />
            <span>Inspector</span>
          </button>

          {/* AI Assistant Copilot Toggle (Opens / Closes like Copilot) */}
          <button
            onClick={() => {
              if (onToggleAIAssistant) {
                onToggleAIAssistant();
              } else {
                setActiveRightTab(activeRightTab === 'ai' ? 'inspector' : 'ai');
              }
            }}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded border transition cursor-pointer ${isAIAssistantOpen && activeRightTab === 'ai'
                ? 'bg-[#261c30] text-[#c084fc] border-[#7c3aed] shadow-xs ring-1 ring-[#7c3aed]/40'
                : 'bg-transparent text-[#7e828e] hover:text-[#c084fc] hover:bg-[#261c30]/40 border-transparent'
              }`}
            title={isAIAssistantOpen && activeRightTab === 'ai' ? "Close AI Copilot Panel" : "Open AI Copilot Panel"}
          >
            <Sparkles className="w-3 h-3 text-[#c084fc] animate-pulse" />
            <span>AI Assistant</span>
            <span className={`text-[8px] font-mono px-1 py-0.2 rounded ${isAIAssistantOpen && activeRightTab === 'ai' ? 'bg-[#392050] text-[#d8b4fe]' : 'bg-[#1e1728] text-[#9378b2]'}`}>
              {isAIAssistantOpen && activeRightTab === 'ai' ? 'Open' : 'Copilot'}
            </span>
          </button>
        </div>
      </div>
    </div>
  );
}
