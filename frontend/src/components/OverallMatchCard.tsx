import { Progress } from "@/components/ui/progress";

export function OverallMatchCard({
  score,
  numberOfMatchedSkills,
  totalSkillsForJob,
}: any) {
  const percentage =
    totalSkillsForJob > 0
      ? (numberOfMatchedSkills / totalSkillsForJob) * 100
      : 0;

  return (
    <div className="flex flex-col w-full mt-10  max-w-5xl bg-amber-500 rounded-t-2xl shadow-xl p-8">
      <p className="text-white ">overall match</p>
      <div className="flex flex-row gap-3 items-center ">
        <span className="text-8xl text-white">{score}</span>
        <span>
          {numberOfMatchedSkills} out of {totalSkillsForJob} skills matched
        </span>
      </div>
      <Progress value={percentage} />
    </div>
  );
}
