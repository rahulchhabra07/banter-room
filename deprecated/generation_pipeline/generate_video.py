import replicate
import os

replicate_client = replicate.Client(os.getenv("REPLICATE_API_KEY"))

def generate_video(outfile = "output.wav"):
    output = replicate_client.run(
        "devxpy/cog-wav2lip:8d65e3f4f4298520e079198b493c25adfc43c058ffec924f2aefc8010ed25eef",
        input={"face": open("richard-feynman.mp4", "rb"), "audio": open(outfile, "rb")}
    )
    print("[FINAL OUT URL]", output)
    return output
