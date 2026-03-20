export function SKillFooterInfo({ color, label, info }: any) {
  return (
    <div className="flex flex-col items-center flex-1">
      <p className={` text-3xl font-bold ${color}`}>{info}</p>
      <p className="text-[10px] text-gray-400 uppercase tracking-widest font-semibold mt-1">
        {label}
      </p>
    </div>
  );
}
