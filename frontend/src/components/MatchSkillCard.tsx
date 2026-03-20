import { CheckCircle2 } from "lucide-react";

export function MatchSkillCard({ skillName }: { skillName: string }) {
  const upperCaseSkillName = skillName.replace(
    skillName[0],
    skillName[0].toUpperCase(),
  );
  return (
    <div className="flex items-center gap-3 p-3 bg-green-50 border-l-4 border-green-500 rounded-r-lg hover:bg-green-100 transition-colors">
      <CheckCircle2 className="w-4 h-4 text-green-600 shrink-0" />
      <span className="text-gray-900 font-medium">{upperCaseSkillName}</span>
    </div>
  );
}
