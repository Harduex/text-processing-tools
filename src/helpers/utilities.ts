import fs from "fs";

export const progressBar = (
  completedCount: number,
  totalCount: number,
  barLength: number = 20
): void => {
  const percentage: number = Math.floor((completedCount / totalCount) * 100);
  const filledBlocks: number = Math.floor((percentage / 100) * barLength);
  const emptyBlocks: number = barLength - filledBlocks;
  const progressBar: string =
    "█".repeat(filledBlocks) + "░".repeat(emptyBlocks);

  const lastBarLength: number = progressBar.length;
  process.stdout.write("\r");
  process.stdout.write(
    `Progress: [${progressBar}] ${percentage}%`.padEnd(lastBarLength + 15)
  );
};

export const getDocuments = (path: string): any => {
  const rawDocuments = fs.readFileSync(path, "utf8");
  const documents: any = JSON.parse(rawDocuments);
  return documents;
};

export const cleanText = (text: string) => {
  return text
    .replace(/[\n\t\r]/g, " ")
    .replace(/\s\s+/g, " ")
    .trim();
};
