export function SkillDisplayCard({
  headline,
  skillsToShow,
  SkillCardToUse,
}: any) {
  return (
    <div className="w-full max-w-2xl bg-white p-8 flex-1">
      <p className="text-center text-1xl font-medium text-gray-700">
        {headline}
      </p>
      <div className="mt-4 flex flex-col gap-3 flex-wrap">
        {skillsToShow.map((skill: string) => {
          return <SkillCardToUse key={skill} skillName={skill} />;
        })}
      </div>
    </div>
  );
}
