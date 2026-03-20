import { SKillFooterInfo } from "./SkillFooterInfo";

export function SkillFooterCard({
  score,
  numberOfSkillsToLearn,
  numberOfMatchedSkills,
}: any) {
  return (
    <div className="w-full max-w-5xl bg-white mx-auto border-t-3 border-gray py-10 rounded-b-2xl">
      <div className="flex flex-row justify-between items-center px-4">
        <SKillFooterInfo
          color="text-amber-500"
          info={score}
          label="Match Score"
        />
        <SKillFooterInfo
          color="text-green-600"
          info={numberOfMatchedSkills}
          label="Skills Found"
        />
        <SKillFooterInfo
          color="text-orange-600"
          info={numberOfSkillsToLearn}
          label="To Develop"
        />
      </div>
    </div>
  );
}
