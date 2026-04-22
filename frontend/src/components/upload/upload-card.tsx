import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { ImageUp } from "lucide-react";

import { Card } from "@/components/common/card";
import { cn } from "@/lib/utils";

export function UploadCard({ onSelect, previewUrl }: { onSelect: (file: File) => void; previewUrl?: string }) {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const [file] = acceptedFiles;
    if (file) {
      onSelect(file);
    }
  }, [onSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [] },
    maxFiles: 1,
  });

  return (
    <Card className="border-gold/15 bg-[#fcf7f0] p-4">
      <div
        {...getRootProps()}
        className={cn(
          "flex min-h-[360px] cursor-pointer flex-col items-center justify-center rounded-[1.75rem] border border-dashed border-charcoal/15 bg-white/70 p-6 text-center transition",
          isDragActive && "border-gold bg-gold/5",
        )}
      >
        <input {...getInputProps()} />
        {previewUrl ? (
          <img src={previewUrl} alt="Portrait preview" className="max-h-[480px] rounded-[1.5rem] object-cover shadow-halo" />
        ) : (
          <>
            <div className="rounded-full border border-gold/20 bg-gold/10 p-4">
              <ImageUp className="h-7 w-7 text-charcoal" />
            </div>
            <p className="mt-6 font-display text-4xl text-charcoal">Upload your portrait</p>
            <p className="mt-3 max-w-md text-sm leading-6 text-charcoal/70">
              One person only. Clear face. Visible neck for necklaces. Visible hand for rings.
            </p>
          </>
        )}
      </div>
    </Card>
  );
}
