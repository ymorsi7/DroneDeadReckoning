document.addEventListener('DOMContentLoaded', (event) => {
    var socket1 = new WebSocket("ws://localhost:6543/ws");
    var socket2 = new WebSocket("ws://localhost:6543/ws_position");

    const takeoffButton = document.getElementById('takeoff');
    const landButton = document.getElementById('land');
    const leftButton = document.getElementById('left');
    const rightButton = document.getElementById('right');
    const forwardButton = document.getElementById('forward');
    const backwardButton = document.getElementById('backward');
    const upButton = document.getElementById('up');
    const downButton = document.getElementById('down');
    const rotateCWButton = document.getElementById('rotateCW');
    const rotateCCWButton = document.getElementById('rotateCCW');

    const commands = {
        takeoff: { command: 'takeoff', name: 'Take Off' },
        land: { command: 'land', name: 'Land' },
        left: { command: 'left', name: 'Move Left' },
        right: { command: 'right', name: 'Move Right' },
        forward: { command: 'forward', name: 'Move Forward' },
        backward: { command: 'backward', name: 'Move Backward' },
        up: { command: 'up', name: 'Move Up' },
        down: { command: 'down', name: 'Move Down' },
        rotateCW: { command: 'rotateCW', name: 'Rotate CW' },
        rotateCCW: { command: 'rotateCCW', name: 'Rotate CCW' }
    };

    const setActiveButton = (button) => {
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
    };

    const sendCommand = (command) => {
        console.log(`Sending command: ${command}`);
        socket1.send(command);
    };

    const addButtonClickListener = (button, command) => {
        button.addEventListener('click', () => {
            setActiveButton(button);
            sendCommand(command.command);
        });
    };

    addButtonClickListener(takeoffButton, commands.takeoff);
    addButtonClickListener(landButton, commands.land);
    addButtonClickListener(leftButton, commands.left);
    addButtonClickListener(rightButton, commands.right);
    addButtonClickListener(forwardButton, commands.forward);
    addButtonClickListener(backwardButton, commands.backward);
    addButtonClickListener(upButton, commands.up);
    addButtonClickListener(downButton, commands.down);
    addButtonClickListener(rotateCWButton, commands.rotateCW);
    addButtonClickListener(rotateCCWButton, commands.rotateCCW);

    var graphContainer = document.getElementById('plot');
    var data = [{
        x: [],
        y: [],
        z: [],
        type: 'scatter3d',
        mode: 'lines',
        line: { color: '#80CAF6' }
    }];
    var layout = {
        title: 'Drone Position',
        xaxis: {
            title: 'X'
        },
        yaxis: {
            title: 'Y'
        },
        zaxis: {
            title: 'Z'
        }
    };
    Plotly.newPlot(graphContainer, data, layout);
    document.addEventListener('keydown', (event) => {
        switch (event.key) {
            case 'ArrowLeft':
                setActiveButton(leftButton);
                sendCommand(commands.left.command);
                break;
            case 'ArrowRight':
                setActiveButton(rightButton);
                sendCommand(commands.right.command);
                break;
            case 'ArrowUp':
                setActiveButton(forwardButton);
                sendCommand(commands.forward.command);
                break;
            case 'ArrowDown':
                setActiveButton(backwardButton);
                sendCommand(commands.backward.command);
                break;
            case 'w':
                setActiveButton(upButton);
                sendCommand(commands.up.command);
                break;
            case 's':
                setActiveButton(downButton);
                sendCommand(commands.down.command);
                break;
            case 'a':
                setActiveButton(rotateCCWButton);
                sendCommand(commands.rotateCCW.command);
                break;
            case 'd':
                setActiveButton(rotateCWButton);
                sendCommand(commands.rotateCW.command);
                break;
            case 't':
                setActiveButton(takeoffButton);
                sendCommand(commands.takeoff.command);
                break;
            case 'l':
                setActiveButton(landButton);
                sendCommand(commands.land.command);
                break;
            default:
                break;
        }
    });

    socket2.addEventListener("message", (event) => {
        var droneState1 = JSON.parse(event.data);
        var droneState2 = JSON.parse(droneState1);
        var update = {
            x: [[droneState2.x]],
            y: [[droneState2.y]],
            z: [[droneState2.z]]
        };
        Plotly.extendTraces(graphContainer, update, [0]);
    });
});
