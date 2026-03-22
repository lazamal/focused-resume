import { Skeleton } from "@/components/ui/skeleton";

export function SkeletonDemo() {
  return (
    <div className="w-full max-w-3xl mt-8 flex flex-col gap-4">
      {/* Overall match card */}
      <div className="bg-white rounded-2xl shadow-xl p-8 space-y-4">
        <Skeleton className="h-6 w-40" />
        <Skeleton className="h-12 w-24" />
        <Skeleton className="h-4 w-64" />
      </div>

      {/* Matched / Missing skills */}
      <div className="flex flex-row gap-4">
        <div className="flex-1 bg-white rounded-2xl shadow-xl p-6 space-y-3">
          <Skeleton className="h-5 w-36" />
          {[...Array(5)].map((_, i) => (
            <Skeleton key={i} className="h-8 w-full rounded-lg" />
          ))}
        </div>
        <div className="flex-1 bg-white rounded-2xl shadow-xl p-6 space-y-3">
          <Skeleton className="h-5 w-36" />
          {[...Array(5)].map((_, i) => (
            <Skeleton key={i} className="h-8 w-full rounded-lg" />
          ))}
        </div>
      </div>

      {/* Footer card */}
      <div className="bg-white rounded-2xl shadow-xl p-6 space-y-3">
        <Skeleton className="h-5 w-48" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-3/4" />
      </div>
    </div>
  );
}
