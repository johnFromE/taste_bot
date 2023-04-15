const { spawn } = require('child_process');

const python = spawn('bash', ['./start.sh']);

python.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

python.stderr.on('data', (data) => {
  console.error(`stderr: ${data}`);
});

python.on('close', (code) => {
  console.log(`child process exited with code ${code}`);
});
