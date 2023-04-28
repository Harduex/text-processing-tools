import { mergeNotesToJson } from "./modules/mergeNotesToJson";
import { convertNotesToTxt } from "./modules/convertNotesToTxt";

(function () {
    const NOTES_DIR: string = process.env.NOTES_DIR || ".";
    const CONVERTED_NOTES_DIR: string = process.env.CONVERTED_NOTES_DIR || ".";
    const OUTPUT_FILENAME: string = process.env.OUTPUT_FILENAME || "notes";

    convertNotesToTxt(NOTES_DIR, `${CONVERTED_NOTES_DIR}/TXT`);
    mergeNotesToJson(NOTES_DIR, `${CONVERTED_NOTES_DIR}/JSON`, OUTPUT_FILENAME);
})();
