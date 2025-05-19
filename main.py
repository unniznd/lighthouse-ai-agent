from lighthouseaiagent import LighthouseAIAgent
from dotenv import load_dotenv

load_dotenv()

agent = LighthouseAIAgent()

summary = agent.upload("files/hello.c")
agent.save(summary)
summary = agent.upload("files/hello.py")
agent.save(summary)


print(agent.query("give me programs that print hello world"))
print(agent.query("python program"))