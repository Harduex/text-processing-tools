import { mergeNotesToJson } from "./modules/mergeNotesToJson";
import { convertNotesToTxt } from "./modules/convertNotesToTxt";

(function () {
    const notesDir: string = process.env.NOTES_DIR || ".";
    const convertedNotesDir: string = process.env.CONVERTED_NOTES_DIR || ".";
    const outputFilename: string = process.env.OUTPUT_FILENAME || "notes";

    convertNotesToTxt(notesDir, `${convertedNotesDir}/TXT`);
    mergeNotesToJson(notesDir, `${convertedNotesDir}/JSON`, outputFilename);
})();
