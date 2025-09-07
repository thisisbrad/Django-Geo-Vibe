# WebSocket Reference

## Connection Protocol

WebSocket connections are established using the WebSocket protocol. The system supports two types of connections:

1. **All Buses**: Connects to receive updates for all buses in the system
2. **Specific Route**: Connects to receive updates for buses on a specific route

## Message Types and Payloads

### Initial Data Message

When a client first connects, an initial data message is sent containing the current state of all relevant buses.

### Bus Location Update Message

As bus locations change, update messages are sent to all connected clients. These messages contain:

- Bus identifier
- Current latitude and longitude
- Speed and heading
- Timestamp

### Bus Status Message

Status messages provide information about bus operational status, such as:

- Active/inactive state
- Route assignment changes
- Maintenance status

## Broadcasting and Channel Groups

The system uses channel groups to efficiently broadcast messages to relevant clients:

- **Global Group**: All connected clients
- **Route Groups**: Clients interested in specific routes

## Frontend Event Handling

The frontend WebSocket service handles several types of events:

- **Connection Open**: Initialize connection and subscribe to relevant groups
- **Message Receive**: Process incoming data and update UI
- **Connection Close**: Handle disconnection gracefully
- **Error Handling**: Manage connection errors and attempt reconnection