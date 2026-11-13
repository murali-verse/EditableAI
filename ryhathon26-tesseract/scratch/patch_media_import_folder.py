from pathlib import Path

target = Path("EditAI/frontend/src/components/MediaImportPanel.jsx")
text = target.read_text(encoding="utf-8")

# 1. Add folderInputRef
old_refs = """  const videoInputRef = useRef(null);
  const audioInputRef = useRef(null);
  const subtitleInputRef = useRef(null);"""

new_refs = """  const videoInputRef = useRef(null);
  const audioInputRef = useRef(null);
  const subtitleInputRef = useRef(null);
  const folderInputRef = useRef(null);"""

assert old_refs in text, "old_refs not found"
text = text.replace(old_refs, new_refs, 1)

# 2. Add clickable folder button in header
old_header = """        {/* Breadcrumb & count */}
        <div className="flex items-center gap-1.5 text-[#c8cbcd]">
          <Folder className="w-3.5 h-3.5 text-[#737887]" />
          <span className="font-medium">Master</span>
          <span className="text-[10px] text-[#636875] font-mono">
            ({mediaPoolVideos.length} clips)
          </span>
        </div>"""

new_header = """        {/* Breadcrumb & count */}
        <div className="flex items-center gap-1.5 text-[#c8cbcd]">
          <button
            onClick={() => folderInputRef.current?.click()}
            className="flex items-center gap-1.5 px-1.5 py-0.5 rounded hover:bg-[#252830] hover:text-white transition group cursor-pointer"
            title="Open Computer Folder (Import All Clips)"
          >
            <Folder className="w-3.5 h-3.5 text-[#737887] group-hover:text-[#38bdf8] transition" />
            <span className="font-medium group-hover:text-white">Master</span>
          </button>
          <span className="text-[10px] text-[#636875] font-mono">
            ({mediaPoolVideos.length} clips)
          </span>
        </div>"""

assert old_header in text, "old_header not found"
text = text.replace(old_header, new_header, 1)

# 3. Add Folder Action Button in right icon group
old_menu_toggle = """          <div className="relative">
            <button
              onClick={() => setIsImportMenuOpen(!isImportMenuOpen)}
              className="p-1 rounded hover:bg-[#252830] hover:text-[#d0d3dc] transition flex items-center gap-0.5"
              title="Import Media Files"
            >
              <Plus className="w-3.5 h-3.5 text-[#b5b9c4]" />
            </button>"""

new_menu_toggle = """          <button
            onClick={() => folderInputRef.current?.click()}
            className="p-1 rounded hover:bg-[#252830] hover:text-[#38bdf8] transition"
            title="Open Computer Folder (Import All Clips)"
          >
            <Folder className="w-3.5 h-3.5 text-[#868d9e] hover:text-[#38bdf8]" />
          </button>

          <div className="relative">
            <button
              onClick={() => setIsImportMenuOpen(!isImportMenuOpen)}
              className="p-1 rounded hover:bg-[#252830] hover:text-[#d0d3dc] transition flex items-center gap-0.5"
              title="Import Media Files"
            >
              <Plus className="w-3.5 h-3.5 text-[#b5b9c4]" />
            </button>"""

assert old_menu_toggle in text, "old_menu_toggle not found"
text = text.replace(old_menu_toggle, new_menu_toggle, 1)

# 4. Add "Open Computer Folder..." in dropdown
old_dropdown = """                <button
                  onClick={() => {
                    setIsImportMenuOpen(false);
                    videoInputRef.current?.click();
                  }}
                  className="w-full text-left px-3 py-1.5 hover:bg-[#252934] text-[#d0d3dc] flex items-center gap-2"
                >
                  <Film className="w-3 h-3 text-[#7f8595]" />
                  <span>Import Videos (Multiple)...</span>
                </button>"""

new_dropdown = """                <button
                  onClick={() => {
                    setIsImportMenuOpen(false);
                    folderInputRef.current?.click();
                  }}
                  className="w-full text-left px-3 py-1.5 hover:bg-[#252934] text-[#d0d3dc] flex items-center gap-2"
                >
                  <Folder className="w-3 h-3 text-[#38bdf8]" />
                  <span>Open Computer Folder...</span>
                </button>
                <button
                  onClick={() => {
                    setIsImportMenuOpen(false);
                    videoInputRef.current?.click();
                  }}
                  className="w-full text-left px-3 py-1.5 hover:bg-[#252934] text-[#d0d3dc] flex items-center gap-2"
                >
                  <Film className="w-3 h-3 text-[#7f8595]" />
                  <span>Import Videos (Multiple)...</span>
                </button>"""

assert old_dropdown in text, "old_dropdown not found"
text = text.replace(old_dropdown, new_dropdown, 1)

# 5. Add folder button in empty state
old_empty = """          <div
            onClick={() => videoInputRef.current?.click()}
            className="h-full flex flex-col items-center justify-center text-center cursor-pointer group p-4 border border-dashed border-[#22242a] rounded"
          >
            <p className="text-[#555a66] text-sm font-normal mb-1 group-hover:text-[#888e9d] transition">
              No clips in media pool
            </p>
            <p className="text-[#3b3e47] text-[11px] group-hover:text-[#555a66] transition">
              Click to select or drop multiple video clips here
            </p>
          </div>"""

new_empty = """          <div
            className="h-full flex flex-col items-center justify-center text-center p-4 border border-dashed border-[#22242a] rounded space-y-2"
          >
            <p className="text-[#555a66] text-sm font-normal mb-0.5">
              No clips in media pool
            </p>
            <p className="text-[#3b3e47] text-[11px] max-w-[220px]">
              Open a computer folder or drop video clips to populate pool
            </p>
            <div className="flex items-center gap-2 pt-1">
              <button
                onClick={() => folderInputRef.current?.click()}
                className="px-2.5 py-1 rounded bg-[#202834] hover:bg-[#2b3748] border border-[#344b68] text-[#7ea5dc] text-[10px] font-medium flex items-center gap-1.5 transition shadow-xs"
              >
                <Folder className="w-3 h-3 text-[#38bdf8]" />
                <span>Open Folder</span>
              </button>
              <button
                onClick={() => videoInputRef.current?.click()}
                className="px-2.5 py-1 rounded bg-[#1c1d22] hover:bg-[#24262d] border border-[#292b33] text-[#b5b9c4] text-[10px] font-medium flex items-center gap-1.5 transition"
              >
                <Film className="w-3 h-3" />
                <span>Select Files</span>
              </button>
            </div>
          </div>"""

assert old_empty in text, "old_empty not found"
text = text.replace(old_empty, new_empty, 1)

# 6. Add hidden folder input
old_inputs = """        {/* Hidden Multiple Video File Input */}
        <input"""

new_inputs = """        {/* Hidden Computer Folder Directory Input */}
        <input
          type="file"
          ref={folderInputRef}
          onChange={(e) => {
            if (e.target.files && e.target.files.length > 0) {
              const validExts = ['.mp4', '.mov', '.webm', '.mkv', '.avi', '.m4v'];
              const videoFiles = Array.from(e.target.files).filter((file) => {
                const ext = '.' + file.name.split('.').pop().toLowerCase();
                return validExts.includes(ext) || file.type.startsWith('video/');
              });
              if (videoFiles.length > 0) {
                onUploadVideos(videoFiles);
              }
            }
            e.target.value = '';
          }}
          webkitdirectory=""
          directory=""
          multiple
          className="hidden"
        />

        {/* Hidden Multiple Video File Input */}
        <input"""

assert old_inputs in text, "old_inputs not found"
text = text.replace(old_inputs, new_inputs, 1)

target.write_text(text, encoding="utf-8")
print("MediaImportPanel.jsx patched with computer folder picker successfully!")

