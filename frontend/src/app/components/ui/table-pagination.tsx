import React from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

export interface TablePaginationProps {
  currentPage: number;
  pageSize: number;
  totalItems: number;
  onPageChange: (page: number) => void;
  onPageSizeChange?: (size: number) => void;
  pageSizeOptions?: number[];
  unitName?: string;
  className?: string;
}

export function TablePagination({
  currentPage,
  pageSize,
  totalItems,
  onPageChange,
  onPageSizeChange,
  pageSizeOptions = [10, 15, 25, 50, 100],
  unitName = "records",
  className = "",
}: TablePaginationProps) {
  const totalPages = Math.max(1, Math.ceil(totalItems / pageSize));
  const safePage = Math.min(Math.max(1, currentPage), totalPages);

  const startRecord = totalItems > 0 ? (safePage - 1) * pageSize + 1 : 0;
  const endRecord = Math.min(safePage * pageSize, totalItems);

  return (
    <div
      className={`flex flex-col sm:flex-row items-center justify-between gap-3 pt-3 border-t border-[#24242F] text-xs text-zinc-400 ${className}`}
    >
      {/* Left: Page Size Selector & Record Count */}
      <div className="flex flex-wrap items-center gap-3">
        {onPageSizeChange && (
          <div className="flex items-center gap-2">
            <span className="text-zinc-400">Show:</span>
            <select
              value={pageSize}
              onChange={(e) => {
                onPageSizeChange(Number(e.target.value));
                onPageChange(1);
              }}
              className="h-8 rounded-lg border border-[#2b2b36] bg-[#141420] px-2 text-xs font-semibold text-white outline-none focus:border-yellow-400"
            >
              {pageSizeOptions.map((opt) => (
                <option key={opt} value={opt}>
                  {opt} {unitName}
                </option>
              ))}
            </select>
          </div>
        )}
        <span className="text-zinc-400">
          Showing <strong className="text-white font-medium">{startRecord}</strong> to{" "}
          <strong className="text-white font-medium">{endRecord}</strong> of{" "}
          <strong className="text-yellow-400 font-bold">{totalItems}</strong> {unitName}
        </span>
      </div>

      {/* Right: Page Navigation Prev / Page Numbers / Next */}
      {totalPages > 1 && (
        <div className="flex items-center gap-1.5 self-end sm:self-auto">
          <button
            type="button"
            onClick={() => onPageChange(Math.max(1, safePage - 1))}
            disabled={safePage <= 1}
            className="flex h-8 items-center gap-1 rounded-lg border border-[#2b2b36] bg-white/[0.03] px-2.5 text-xs font-semibold text-white/70 transition hover:bg-white/[0.08] hover:text-white disabled:cursor-not-allowed disabled:opacity-30"
          >
            <ChevronLeft className="h-3.5 w-3.5" />
            <span>Prev</span>
          </button>

          <div className="flex items-center gap-1">
            {Array.from({ length: totalPages }, (_, i) => i + 1)
              .filter((page) => {
                if (totalPages <= 7) return true;
                if (page === 1 || page === totalPages) return true;
                return Math.abs(page - safePage) <= 1;
              })
              .map((page, idx, arr) => {
                const prev = arr[idx - 1];
                const hasGap = prev && page - prev > 1;
                return (
                  <div key={page} className="flex items-center">
                    {hasGap && <span className="px-1 text-xs text-white/30">...</span>}
                    <button
                      type="button"
                      onClick={() => onPageChange(page)}
                      className={`h-8 min-w-[32px] rounded-lg px-2 text-xs font-semibold transition ${
                        safePage === page
                          ? "bg-yellow-400 text-black font-bold shadow"
                          : "border border-[#2b2b36] bg-white/[0.03] text-white/70 hover:bg-white/[0.08] hover:text-white"
                      }`}
                    >
                      {page}
                    </button>
                  </div>
                );
              })}
          </div>

          <button
            type="button"
            onClick={() => onPageChange(Math.min(totalPages, safePage + 1))}
            disabled={safePage >= totalPages}
            className="flex h-8 items-center gap-1 rounded-lg border border-[#2b2b36] bg-white/[0.03] px-2.5 text-xs font-semibold text-white/70 transition hover:bg-white/[0.08] hover:text-white disabled:cursor-not-allowed disabled:opacity-30"
          >
            <span>Next</span>
            <ChevronRight className="h-3.5 w-3.5" />
          </button>
        </div>
      )}
    </div>
  );
}

