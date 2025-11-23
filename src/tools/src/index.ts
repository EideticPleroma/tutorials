import * as fs from 'fs';
import * as path from 'path';

const args = process.argv.slice(2);
const command = args[0];

async function handleCommand() {
    switch (command) {
        case 'read_file':
            const filePath = args[1];
            if (!filePath) {
                console.error('Error: File path required');
                process.exit(1);
            }
            try {
                // Security check: prevent reading outside of allowed paths in a real app
                // For tutorial, just read it.
                const content = fs.readFileSync(filePath, 'utf-8');
                console.log(content);
            } catch (error: any) {
                console.error(`Error reading file: ${error.message}`);
                process.exit(1);
            }
            break;
        
        case 'list_dir':
            const dirPath = args[1] || '.';
            try {
                const files = fs.readdirSync(dirPath);
                console.log(JSON.stringify(files));
            } catch (error: any) {
                console.error(`Error listing directory: ${error.message}`);
                process.exit(1);
            }
            break;

        default:
            console.error(`Unknown command: ${command}`);
            console.error('Available commands: read_file <path>, list_dir <path>');
            process.exit(1);
    }
}

handleCommand();

