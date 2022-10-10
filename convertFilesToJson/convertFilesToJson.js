const path = require('path');
const fs = require('fs');
const async = require('async');
const yargs = require('yargs/yargs')
const { hideBin } = require('yargs/helpers')

/**
 * This script converts list of txt files in directory to array in json file
 */

const argv = yargs(hideBin(process.argv)).argv;
const [inputDir, outputDir, outputFilename] = [argv.input || '.', argv.output || '.', argv.filename || 'notes'];

function convertFilesToJson(inputDir, outputDir, outputFilename) {

    function readAsync(filename, callback) {
        fs.readFile(`${inputDir}/${filename}`, 'utf8', callback);
    }

    fs.readdir(inputDir, function (err, filenames) {
        if (err) {
            return console.log('Unable to scan directory: ' + err);
        }

        async.map(filenames, readAsync, (err, filesList) => {

            const jsonData = {
                data: filesList
            }

            if (!fs.existsSync(outputDir)) {
                fs.mkdirSync(outputDir, { recursive: true });
            }

            fs.writeFile(`${outputDir}/${outputFilename}.json`, JSON.stringify(jsonData, null, 2), 'utf8', function (err) {
                if (err) return console.log(err);
                console.log(`Done. Check your generated json file at '${outputDir}/${outputFilename}.json'`);
            });

        });

    });
}

(function () {
    convertFilesToJson(inputDir, outputDir, outputFilename)
})();