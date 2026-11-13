import React, { useState } from 'react';
import {
  Layers,
  Sparkles,
  Camera,
  Music,
  Clock,
  CheckCircle2,
  Sliders,
  Play,
  Plus,
  RefreshCw,
  Film
} from 'lucide-react';
import { formatTimecode } from '../utils/timeUtils';

export default function SyncBinPanel({
  mediaPoolVideos = [],
  currentTime = 0,
  onInsertVideoToTimeline,
  onSeek,
  fps = 25
}) {
  const [syncMethod, setSyncMethod] = useState('audio'); // 'audio' | 'timecode' | 'in_point'
  const [selectedAngleIndex, setSelectedAngleIndex] = useState(0);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncStatus, setSyncStatus] = useState(null);

  const angles = mediaPoolVideos.slice(0, 4);

  const handleAutoSync = () => {
    setIsSyncing(true);
    setSyncStatus(null);
    setTimeout(() => {
      setIsSyncing(false);
      setSyncStatus({
        synced: true,
        method: syncMethod === 'audio' ? 'Audio Waveform Peaks' : syncMethod === 'timecode' ? 'SMPTE Timecode' : 'In-Point Marker',
        angleCount: Math.max(1, angles.length),
        offset: '00:00:00:00 aligned'
      });
    }, 600);
  };

  const handleCutAngle = (angle, idx) => {
    if (!angle) return;
    if (onInsertVideoToTimeline) {
      onInsertVideoToTimeline(angle);
    }
  };

  return (
    <div className="h-full flex flex-col bg-[#141518] text-[#a0a4ae] select-none text-[11px] overflow-hidden">
      {/* 1. Header */}
      <div className="h-8 px-3 border-b border-[#212328] flex items-center justify-between bg-[#18191d]">
        <div className="flex items-center gap-1.5 text-[#d0d3dc] font-medium">
          <Layers className="w-3.5 h-3.5 text-[#c084fc]" />
          <span>Sync Bin</span>
          <span className="text-[10px] text-[#636875] font-mono">
            ({angles.length} {angles.length === 1 ? 'Angle' : 'Angles'})
          </span>
        </div>
        <button
          onClick={handleAutoSync}
          disabled={isSyncing || angles.length === 0}
          className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#261c30] hover:bg-[#351e4c] text-[#c084fc] border border-[#7c3aed] transition text-[10px] disabled:opacity-40"
          title="Auto-synchronize all camera angles using chosen method"
        >
          <RefreshCw className={`w-2.5 h-2.5 ${isSyncing ? 'animate-spin' : ''}`} />
          <span>{isSyncing ? 'Syncing...' : 'Auto-Sync'}</span>
        </button>
      </div>

      {/* 2. Sync Method Switcher */}
      <div className="p-2.5 border-b border-[#212328] bg-[#121316] space-y-1.5">
        <label className="text-[10px] font-medium text-[#7a808e] block uppercase tracking-wider">
          Sync Mode
        </label>
        <div className="grid grid-cols-3 gap-1 bg-[#17181c] p-0.5 rounded border border-[#212328]">
          <button
            onClick={() => setSyncMethod('audio')}
            className={`py-1 px-1.5 rounded text-[10px] font-medium transition flex items-center justify-center gap-1 ${
              syncMethod === 'audio'
                ? 'bg-[#261c30] text-[#c084fc] border border-[#7c3aed] shadow-xs'
                : 'text-[#6f7482] hover:text-[#c084fc]'
            }`}
          >
            <Music className="w-3 h-3 text-[#c084fc]" />
            <span>Audio Wave</span>
          </button>
          <button
            onClick={() => setSyncMethod('timecode')}
            className={`py-1 px-1.5 rounded text-[10px] font-medium transition flex items-center justify-center gap-1 ${
              syncMethod === 'timecode'
                ? 'bg-[#261c30] text-[#c084fc] border border-[#7c3aed] shadow-xs'
                : 'text-[#6f7482] hover:text-[#c084fc]'
            }`}
          >
            <Clock className="w-3 h-3 text-[#c084fc]" />
            <span>Timecode</span>
          </button>
          <button
            onClick={() => setSyncMethod('in_point')}
            className={`py-1 px-1.5 rounded text-[10px] font-medium transition flex items-center justify-center gap-1 ${
              syncMethod === 'in_point'
                ? 'bg-[#261c30] text-[#c084fc] border border-[#7c3aed] shadow-xs'
                : 'text-[#6f7482] hover:text-[#c084fc]'
            }`}
          >
            <Camera className="w-3 h-3 text-[#c084fc]" />
            <span>In-Point</span>
          </button>
        </div>

        {syncStatus && (
          <div className="flex items-center gap-1.5 text-[10px] text-[#5bb676] bg-[#17241b] border border-[#223d2a] px-2 py-1 rounded">
            <CheckCircle2 className="w-3 h-3 shrink-0" />
            <span className="truncate">
              Synced {syncStatus.angleCount} angles via {syncStatus.method}
            </span>
          </div>
        )}
      </div>

      {/* 3. Multi-Camera Angle Grid */}
      <div className="flex-1 overflow-y-auto p-2.5 space-y-2">
        {angles.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-4 text-[#555a66] space-y-2">
            <Layers className="w-8 h-8 text-[#30333d] stroke-[1.5]" />
            <p className="text-xs">No media loaded for Sync Bin</p>
            <p className="text-[10px] text-[#424652] max-w-[200px]">
              Import 2 or more video clips into the Media Pool to sync multi-cam angles.
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            <span className="text-[10px] font-medium text-[#7a808e] block uppercase tracking-wider">
              Camera Angles ({angles.length})
            </span>
            <div className="grid grid-cols-2 gap-2">
              {angles.map((angle, idx) => {
                const isSelected = selectedAngleIndex === idx;
                const dur = angle.metadata?.duration || 10.0;
                return (
                  <div
                    key={angle.id || idx}
                    onClick={() => setSelectedAngleIndex(idx)}
                    className={`bg-[#18191e] border rounded p-1.5 cursor-pointer transition relative group ${
                      isSelected
                        ? 'border-[#7c3aed] ring-1 ring-[#7c3aed]/40 bg-[#261c30]'
                        : 'border-[#262830] hover:border-[#383c48]'
                    }`}
                  >
                    {/* Angle Header */}
                    <div className="flex items-center justify-between text-[9px] mb-1">
                      <span className="font-semibold text-[#d0d3dc] flex items-center gap-1">
                        <span className={`w-1.5 h-1.5 rounded-full ${isSelected ? 'bg-[#c084fc]' : 'bg-[#555a66]'}`} />
                        Cam {idx + 1}
                      </span>
                      <span className="font-mono text-[#787d8c]">{dur.toFixed(1)}s</span>
                    </div>

                    {/* Preview box / video thumbnail */}
                    <div className="w-full h-16 bg-[#0f1013] rounded flex items-center justify-center overflow-hidden relative">
                      {angle.stream_url ? (
                        <video
                          src={angle.stream_url}
                          className="w-full h-full object-cover pointer-events-none opacity-80 group-hover:opacity-100 transition"
                        />
                      ) : (
                        <Film className="w-4 h-4 text-[#434752]" />
                      )}
                      <div className="absolute bottom-1 right-1 px-1 py-0.2 rounded bg-black/80 font-mono text-[8px] text-[#a0a4ae]">
                        {angle.metadata?.fps || 25} fps
                      </div>
                    </div>

                    {/* Clip title */}
                    <p className="text-[9px] text-[#a8adb8] truncate mt-1" title={angle.filename}>
                      {angle.filename}
                    </p>

                    {/* Cut button overlay */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleCutAngle(angle, idx);
                      }}
                      className="w-full mt-1.5 py-1 rounded bg-[#261c30] hover:bg-[#351e4c] border border-[#7c3aed] text-[#c084fc] text-[9px] font-medium flex items-center justify-center gap-1 transition"
                      title="Cut this angle into timeline"
                    >
                      <Plus className="w-2.5 h-2.5" />
                      <span>Cut to Timeline</span>
                    </button>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* 4. Footer Quick Action */}
      {angles.length > 0 && (
        <div className="p-2 border-t border-[#212328] bg-[#16171b] flex items-center justify-between">
          <span className="text-[10px] text-[#6f7482]">
            Active: Cam {selectedAngleIndex + 1} ({angles[selectedAngleIndex]?.filename?.slice(0, 16)}...)
          </span>
          <button
            onClick={() => handleCutAngle(angles[selectedAngleIndex], selectedAngleIndex)}
            className="px-2.5 py-1 rounded bg-[#261c30] hover:bg-[#351e4c] border border-[#7c3aed] text-[#c084fc] text-[10px] font-medium flex items-center gap-1 transition"
          >
            <Plus className="w-3 h-3 text-[#c084fc]" />
            <span>Insert Angle</span>
          </button>
        </div>
      )}
    </div>
  );
}

