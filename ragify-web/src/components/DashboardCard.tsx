import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

interface DashboardCardProps {
  title: string;
  value: number | string;
  description?: string;
  theme?: "light" | "dark"; // optional, defaults to dark
}

export default function DashboardCard({
  title,
  value,
  description,
  theme = "dark", // <-- set default to dark
}: DashboardCardProps) {
  const baseClasses = "w-full rounded-lg border p-4 hover:shadow-xl transition-shadow";
  const lightClasses = "bg-white border-gray-200 text-gray-900";
  const darkClasses = "bg-gray-800 border-gray-700 text-white";

  return (
    <Card className={`${baseClasses} ${theme === "dark" ? darkClasses : lightClasses}`}>
      <CardHeader>
        <CardTitle className="text-sm text-gray-500 dark:text-gray-400">{title}</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col items-center justify-center">
        <p className="text-3xl font-extrabold">{value}</p>
        {description && <p className="text-sm mt-1 text-center">{description}</p>}
      </CardContent>
    </Card>
  );
}
