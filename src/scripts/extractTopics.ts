import { extractTopics } from "../modules/extractTopics";

(async function () {
  const convertedNotesDir: string =
    `${process.env.CONVERTED_NOTES_DIR}/JSON` || ".";
    
  await extractTopics(convertedNotesDir);
})();
