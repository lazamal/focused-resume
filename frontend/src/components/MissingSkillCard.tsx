import { XCircle } from "lucide-react";

export function MissingSkillCard({ skillName }: { skillName: string }) {
  const upperCaseSkillName = skillName.replace(
    skillName[0],
    skillName[0].toUpperCase(),
  );
  return (
    <div className="flex items-center gap-3 p-3 bg-orange-50 border-l-4 border-orange-500 rounded-r-lg hover:bg-orange-100 transition-colors">
      <XCircle className="w-4 h-4 text-orange-600 shrink-0" />
      <span className="text-gray-900 font-medium">{upperCaseSkillName}</span>
    </div>
  );
}
