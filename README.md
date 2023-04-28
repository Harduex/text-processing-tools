## Text Processing Tools

This project is a collection of text processing tools, specifically designed to work with Google Keep notes exports. It allows users to convert their notes into different formats with ease. The project is written in TypeScript and Node.js.

### Features

The following features are currently available in the project:

- Conversion of Google Keep notes to plain TXT format.
- Merging of multiple Google Keep notes into a single JSON array.

### Installation

To install the project, please follow the steps below:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run `nvm use` if you have nvm to select the right node version for the project.
4. Run `npm install` to install the project dependencies.
5. Create `.env` file from example and update the environment variables: `cp .env.example .env`

### Usage
1. Place your Google Keep notes exports in the Data/Notes directory. Alternatively, set the path to your notes directory using the NOTES_DIR environment variable. For example, NOTES_DIR=../Takeout/Keep.
3. Run `tsc:build` to build the project.
3. Run `npm run start` to convert the notes to all available formats.
4. The converted notes will be saved in the `Data/Converted` directory or the path configured in `CONVERTED_NOTES_DIR=../Converted` in their respective formats.

### Environment Variables

The following environment variables are available in the project:

- `NOTES_DIR`: Specifies the directory where the Google Keep notes exports are stored. Default value is `.`.
- `CONVERTED_NOTES_DIR`: Specifies the directory where the converted notes will be saved. Default value is `.`.
- `OUTPUT_FILENAME`: Specifies the name of the output json file for the merged notes. Default value is `notes`.

### Scripts

The following scripts are available in the project:

- `notes:convert:txt`: Converts Google Keep notes to TXT format.
- `notes:merge:json`: Converts Google Keep notes to JSON format.

The `Data` directory contains the input and output files. The `dist` directory contains the compiled TypeScript files. The `node_modules` directory contains the project dependencies. The `src` directory contains the TypeScript files.