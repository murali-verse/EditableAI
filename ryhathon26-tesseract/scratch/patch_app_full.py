from pathlib import Path

target = Path("EditAI/frontend/src/App.jsx")
text = target.read_text(encoding="utf-8")

# 1. Add component imports
old_imports = """import MultiVideoAssemblyStage from './components/MultiVideoAssemblyStage';"""

new_imports = """import MultiVideoAssemblyStage from './components/MultiVideoAssemblyStage';
import SyncBinPanel from './components/SyncBinPanel';
import TransitionsPanel from './components/TransitionsPanel';
import TitlesPanel from './components/TitlesPanel';
import EffectsPanel from './components/EffectsPanel';"""

assert old_imports in text, "old_imports not found"
text = text.replace(old_imports, new_imports, 1)

# 2. Add activeLeftTab, isRightPanelOpen, globalFolderInputRef, persistent chatMessages
old_chat_state = """  // Analysis & Inspector state
  const [analysis, setAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [activeRightTab, setActiveRightTab] = useState('ai'); // 'inspector' | 'ai'

  // AI Assistant Chat state
  const [chatMessages, setChatMessages] = useState([
    {
      id: 'init_1',
      sender: 'assistant',
      text: 'REELCRAFT AI ready. You can describe any edit in natural language, for example:\\n• "Select the clip from 00:10 to 00:25."\\n• "Split at 00:18."\\n• "Delete the selected segment."\\n• "Delete the second half of the selected clip."\\n• "Export the edited video."',
      timestamp: 'Ready',
    },
  ]);
  const [isChatProcessing, setIsChatProcessing] = useState(false);"""

new_chat_state = """  // Analysis & Inspector state
  const [analysis, setAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [activeRightTab, setActiveRightTab] = useState('ai'); // 'inspector' | 'ai'
  const [activeLeftTab, setActiveLeftTab] = useState('media'); // 'media' | 'sync_bin' | 'transitions' | 'titles' | 'effects'
  const [isRightPanelOpen, setIsRightPanelOpen] = useState(true); // Copilot panel toggle
  const globalFolderInputRef = useRef(null);

  // AI Assistant Chat state (Persisted in localStorage across Copilot open/close toggles)
  const [chatMessages, setChatMessages] = useState(() => {
    try {
      const saved = localStorage.getItem('editmind_copilot_history');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      }
    } catch (e) {}
    return [
      {
        id: 'init_1',
        sender: 'assistant',
        text: 'REELCRAFT AI Copilot ready. You can describe any edit in natural language, for example:\\n• "Select the clip from 00:10 to 00:25."\\n• "Split at 00:18."\\n• "Delete the selected segment."\\n• "Delete the second half of the selected clip."\\n• "Export the edited video."',
        timestamp: 'Ready',
      },
    ];
  });
  const [isChatProcessing, setIsChatProcessing] = useState(false);

  // Save conversation history whenever chatMessages updates
  useEffect(() => {
    try {
      localStorage.setItem('editmind_copilot_history', JSON.stringify(chatMessages));
    } catch (e) {}
  }, [chatMessages]);"""

assert old_chat_state in text, "old_chat_state not found"
text = text.replace(old_chat_state, new_chat_state, 1)

# 3. Add handler functions for Copilot toggle, Transition, Title, Effect, Folder
old_handlers_anchor = """  // Keyboard Shortcuts
  useEffect(() => {"""

new_handlers = """  // Toggle AI Assistant Copilot Open / Close (like Copilot drawer)
  const handleToggleAIAssistant = () => {
    if (isRightPanelOpen && activeRightTab === 'ai') {
      setIsRightPanelOpen(false);
    } else {
      setIsRightPanelOpen(true);
      setActiveRightTab('ai');
    }
  };

  // Trigger computer folder picker
  const handleOpenComputerFolder = () => {
    globalFolderInputRef.current?.click();
  };

  // Handle video transitions from TransitionsPanel
  const handleApplyTransition = (transitionData) => {
    if (!timeline.clips || timeline.clips.length === 0) return;
    const targetId = timeline.selected_clip_id || timeline.clips[0].id;
    const updatedClips = timeline.clips.map((c) => {
      if (transitionData.targetScope === 'all' || c.id === targetId) {
        return {
          ...c,
          transition: transitionData,
          transitionLabel: `${transitionData.name} (${transitionData.duration}s)`,
        };
      }
      return c;
    });
    setTimeline((prev) => ({ ...prev, clips: updatedClips }));
    setIsEdited(true);
    addChatMessage(
      'assistant',
      `✨ Applied "${transitionData.name}" transition (${transitionData.duration}s) to ${
        transitionData.targetScope === 'all' ? 'all timeline cuts' : 'selected cut'
      }.`
    );
  };

  // Handle titles and lower thirds from TitlesPanel
  const handleInsertTitle = (titleData) => {
    const newSub = {
      id: Date.now(),
      start_time: Math.round(titleData.startTime * 100) / 100,
      end_time: Math.round(titleData.endTime * 100) / 100,
      text: titleData.fullText,
      color: titleData.color,
      style: titleData.templateId,
    };
    const updatedSubs = [...(subtitles || []), newSub].sort((a, b) => a.start_time - b.start_time);
    setSubtitles(updatedSubs);
    setTimeline((prev) => ({
      ...prev,
      subtitles: updatedSubs,
    }));
    setIsEdited(true);
    addChatMessage(
      'assistant',
      `📝 Inserted title "${titleData.title}" from ${newSub.start_time.toFixed(1)}s to ${newSub.end_time.toFixed(1)}s on Subtitle Track (Sub1).`
    );
  };

  // Handle color grades and FX from EffectsPanel
  const handleApplyEffect = (effectData) => {
    if (!timeline.clips || timeline.clips.length === 0) return;
    const targetId = timeline.selected_clip_id || timeline.clips[0].id;
    const updatedClips = timeline.clips.map((c) => {
      if (effectData.targetScope === 'all' || c.id === targetId) {
        return {
          ...c,
          filter: effectData.cssFilter,
          effectName: effectData.name,
        };
      }
      return c;
    });
    setTimeline((prev) => ({ ...prev, clips: updatedClips }));
    setIsEdited(true);
    addChatMessage(
      'assistant',
      `🎨 Applied visual effect "${effectData.name}" to ${
        effectData.targetScope === 'all' ? 'all sequence clips' : 'selected clip'
      }.`
    );
  };

  // Keyboard Shortcuts
  useEffect(() => {"""

assert old_handlers_anchor in text, "old_handlers_anchor not found"
text = text.replace(old_handlers_anchor, new_handlers, 1)

# 4. Update JSX for Navbar and Left/Right panels
old_workspace_jsx = """      {/* 1. DaVinci Resolve Top Navigation & Toolbar */}
      <Navbar
        projectName={projectName}
        onSaveProject={handleSaveProject}
        onNewProject={() => setIsProjectModalOpen(true)}
        onOpenProjectList={() => setIsProjectModalOpen(true)}
        onAnalyze={handleAnalyze}
        isAnalyzing={isAnalyzing}
        onOpenExport={() => setIsExportOpen(true)}
        onOpenAssemblyStage={() => setIsAssemblyStageOpen(true)}
        onLoadSample={handleLoadSample}
        hasMedia={!!videoMetadata}
        activeRightTab={activeRightTab}
        setActiveRightTab={setActiveRightTab}
        isEdited={isEdited}
      />

      {/* 2. Middle Main Workspace (Media Pool | Video Viewer | Inspector/AI) */}
      <div className="flex-1 flex overflow-hidden min-h-0 border-b border-[#212328]">
        {/* Left: Media Pool */}
        <div className="w-80 shrink-0 h-full border-r border-[#212328]">
          <MediaImportPanel
            mediaPoolVideos={mediaPoolVideos}
            activeVideoId={activeVideoId}
            audioTrack={audioTrack}
            subtitles={subtitles}
            onUploadVideos={handleUploadVideos}
            onUploadAudio={handleUploadAudio}
            onUploadSubtitle={handleUploadSubtitle}
            onRemoveVideo={handleRemoveMediaPoolVideo}
            onRemoveMedia={handleRemoveMedia}
            onSelectVideo={handleSelectVideo}
            onInsertVideoToTimeline={handleInsertVideoToTimeline}
          />
        </div>

        {/* Center: Video Viewer */}
        <div className="flex-1 h-full flex flex-col min-w-0">
          <VideoPlayer
            videoSrc={videoSrc}
            timeline={timeline}
            currentTime={currentTime}
            onTimeUpdate={setCurrentTime}
            isPlaying={isPlaying}
            setIsPlaying={setIsPlaying}
            subtitles={subtitles}
            playbackRange={playbackRange}
            onPlaybackComplete={() => setPlaybackRange(null)}
            fps={videoMetadata?.fps || 25}
          />
        </div>

        {/* Right: Inspector & AI Assistant Panel */}
        <div className="w-80 shrink-0 h-full border-l border-[#212328] flex flex-col bg-[#141518]">
          <div className="flex-1 overflow-hidden">
            {activeRightTab === 'inspector' ? (
              <Inspector
                selectedClip={selectedClip}
                timeline={timeline}
                analysis={analysis}
                assemblyResult={assemblyResult}
                onSeekToScene={handleSeekToScene}
                onUpdateClipSpeed={(id, spd) => {
                  setTimeline((prev) => ({
                    ...prev,
                    clips: prev.clips.map((c) => (c.id === id ? { ...c, speed: spd } : c)),
                  }));
                  setIsEdited(true);
                }}
                onUpdateClipVolume={(id, vol) => {
                  setTimeline((prev) => ({
                    ...prev,
                    clips: prev.clips.map((c) => (c.id === id ? { ...c, volume: vol } : c)),
                  }));
                  setIsEdited(true);
                }}
                videoMetadata={videoMetadata}
              />
            ) : (
              <AIChatbotPanel
                chatMessages={chatMessages}
                onSendCommand={handleSendCommand}
                isProcessing={isChatProcessing}
                onSelectSuggestion={(cmd) => handleSendCommand(cmd)}
                onApplyProposal={() => {}}
                onCancelProposal={() => {}}
              />
            )}
          </div>
        </div>
      </div>"""

new_workspace_jsx = """      {/* 1. DaVinci Resolve Top Navigation & Toolbar */}
      <Navbar
        projectName={projectName}
        onSaveProject={handleSaveProject}
        onNewProject={() => setIsProjectModalOpen(true)}
        onOpenProjectList={() => setIsProjectModalOpen(true)}
        onAnalyze={handleAnalyze}
        isAnalyzing={isAnalyzing}
        onOpenExport={() => setIsExportOpen(true)}
        onOpenAssemblyStage={() => setIsAssemblyStageOpen(true)}
        onLoadSample={handleLoadSample}
        onOpenFolder={handleOpenComputerFolder}
        hasMedia={!!videoMetadata}
        activeRightTab={activeRightTab}
        setActiveRightTab={(tab) => {
          setActiveRightTab(tab);
          setIsRightPanelOpen(true);
        }}
        isAIAssistantOpen={isRightPanelOpen}
        onToggleAIAssistant={handleToggleAIAssistant}
        activeLeftTab={activeLeftTab}
        setActiveLeftTab={setActiveLeftTab}
        isEdited={isEdited}
      />

      {/* 2. Middle Main Workspace (Left Tool Panel | Video Viewer | Right Copilot/Inspector) */}
      <div className="flex-1 flex overflow-hidden min-h-0 border-b border-[#212328]">
        {/* Left Panel: Media Pool | Sync Bin | Transitions | Titles | Effects */}
        <div className="w-80 shrink-0 h-full border-r border-[#212328]">
          {activeLeftTab === 'media' && (
            <MediaImportPanel
              mediaPoolVideos={mediaPoolVideos}
              activeVideoId={activeVideoId}
              audioTrack={audioTrack}
              subtitles={subtitles}
              onUploadVideos={handleUploadVideos}
              onUploadAudio={handleUploadAudio}
              onUploadSubtitle={handleUploadSubtitle}
              onRemoveVideo={handleRemoveMediaPoolVideo}
              onRemoveMedia={handleRemoveMedia}
              onSelectVideo={handleSelectVideo}
              onInsertVideoToTimeline={handleInsertVideoToTimeline}
            />
          )}
          {activeLeftTab === 'sync_bin' && (
            <SyncBinPanel
              mediaPoolVideos={mediaPoolVideos}
              currentTime={currentTime}
              onInsertVideoToTimeline={handleInsertVideoToTimeline}
              onSeek={setCurrentTime}
              fps={videoMetadata?.fps || 25}
            />
          )}
          {activeLeftTab === 'transitions' && (
            <TransitionsPanel
              timeline={timeline}
              onApplyTransition={handleApplyTransition}
            />
          )}
          {activeLeftTab === 'titles' && (
            <TitlesPanel
              currentTime={currentTime}
              onInsertTitle={handleInsertTitle}
            />
          )}
          {activeLeftTab === 'effects' && (
            <EffectsPanel
              selectedClip={selectedClip}
              timeline={timeline}
              onApplyEffect={handleApplyEffect}
            />
          )}
        </div>

        {/* Center: Video Viewer (Expands to full width when Copilot is closed) */}
        <div className="flex-1 h-full flex flex-col min-w-0">
          <VideoPlayer
            videoSrc={videoSrc}
            timeline={timeline}
            currentTime={currentTime}
            onTimeUpdate={setCurrentTime}
            isPlaying={isPlaying}
            setIsPlaying={setIsPlaying}
            subtitles={subtitles}
            playbackRange={playbackRange}
            onPlaybackComplete={() => setPlaybackRange(null)}
            fps={videoMetadata?.fps || 25}
          />
        </div>

        {/* Right: Inspector & AI Assistant Copilot Panel (Toggles open/close like Copilot) */}
        {isRightPanelOpen && (
          <div className="w-80 shrink-0 h-full border-l border-[#212328] flex flex-col bg-[#141518] transition-all duration-200">
            <div className="flex-1 overflow-hidden">
              {activeRightTab === 'inspector' ? (
                <Inspector
                  selectedClip={selectedClip}
                  timeline={timeline}
                  analysis={analysis}
                  assemblyResult={assemblyResult}
                  onSeekToScene={handleSeekToScene}
                  onUpdateClipSpeed={(id, spd) => {
                    setTimeline((prev) => ({
                      ...prev,
                      clips: prev.clips.map((c) => (c.id === id ? { ...c, speed: spd } : c)),
                    }));
                    setIsEdited(true);
                  }}
                  onUpdateClipVolume={(id, vol) => {
                    setTimeline((prev) => ({
                      ...prev,
                      clips: prev.clips.map((c) => (c.id === id ? { ...c, volume: vol } : c)),
                    }));
                    setIsEdited(true);
                  }}
                  videoMetadata={videoMetadata}
                />
              ) : (
                <AIChatbotPanel
                  chatMessages={chatMessages}
                  onSendCommand={handleSendCommand}
                  isProcessing={isChatProcessing}
                  onSelectSuggestion={(cmd) => handleSendCommand(cmd)}
                  onApplyProposal={() => {}}
                  onCancelProposal={() => {}}
                  onCloseCopilot={() => setIsRightPanelOpen(false)}
                />
              )}
            </div>
          </div>
        )}
      </div>"""

assert old_workspace_jsx in text, "old_workspace_jsx not found"
text = text.replace(old_workspace_jsx, new_workspace_jsx, 1)

# 5. Add hidden global folder input before modals
old_modals = """      {/* 5. Modals */}"""
new_modals = """      {/* Hidden Global Computer Folder Directory Input */}
      <input
        type="file"
        ref={globalFolderInputRef}
        onChange={(e) => {
          if (e.target.files && e.target.files.length > 0) {
            const validExts = ['.mp4', '.mov', '.webm', '.mkv', '.avi', '.m4v'];
            const videoFiles = Array.from(e.target.files).filter((file) => {
              const ext = '.' + file.name.split('.').pop().toLowerCase();
              return validExts.includes(ext) || file.type.startsWith('video/');
            });
            if (videoFiles.length > 0) {
              handleUploadVideos(videoFiles);
            }
          }
          e.target.value = '';
        }}
        webkitdirectory=""
        directory=""
        multiple
        className="hidden"
      />

      {/* 5. Modals */}"""

assert old_modals in text, "old_modals not found"
text = text.replace(old_modals, new_modals, 1)

target.write_text(text, encoding="utf-8")
print("App.jsx updated with Sync Bin, Transitions, Titles, Effects, Folder & Copilot toggle successfully!")

