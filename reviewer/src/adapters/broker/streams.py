from faststream.nats import JStream

cmd = JStream("cmd", declare=False)
events = JStream("events", declare=False)
