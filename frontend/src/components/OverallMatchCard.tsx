import { Progress } from "@/components/ui/progress";

export function OverallMatchCard() {
  return (
    <div className="flex flex-col w-full mt-10  max-w-5xl bg-amber-500 rounded-t-2xl shadow-xl p-8">
      <p className="text-white ">overall match</p>
      <div className="flex flex-row gap-3 items-center ">
        <span className="text-8xl text-white">75%</span>
        <span>3 out of 10 skills matched</span>
      </div>
      <Progress value={75} />
    </div>
  );
}
