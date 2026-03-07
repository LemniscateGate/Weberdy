from uagents import Agent, Context, Model

class Message(Model):
    text: str

agent = Agent(
    name="weberdy",
    port=8001,
    seed="weberdy autonomous node seed phrase",
    endpoint=["http://127.0.0.1:8001"]
)

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("Weberdy agent is online.")

@agent.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.text}")

if __name__ == "__main__":
    agent.run()
