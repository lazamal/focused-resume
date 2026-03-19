export function SkillCard({ skillName }: { skillName: string }) {
  const upperCaseSkillName = skillName.replace(
    skillName[0],
    skillName[0].toUpperCase(),
  );
  return (
    <span className="inline-block px-3 py-1 border-2 border-gray-700 shadow-xl shadow-black/40 rounded-full bg-white text-gray-800 text-sm font-medium">
      {upperCaseSkillName}
    </span>
  );
}
