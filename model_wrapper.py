import torch
import tiktoken
from model import GPTConfig, GPT
from contextlib import nullcontext

class DiscordGPT:
    def __init__(self, checkpoint_path='out-discord/ckpt.pt', device='cuda'):
        self.device = device
        self.ctx = nullcontext() if device == 'cpu' else torch.amp.autocast(device_type=device, dtype=torch.bfloat16)
        
        # Load model
        checkpoint = torch.load(checkpoint_path, map_location=device)
        gptconf = GPTConfig(**checkpoint['model_args'])
        self.model = GPT(gptconf)
        self.model.load_state_dict(checkpoint['model'])
        self.model.eval()
        self.model.to(device)
        
        # Load OpenAI tokenizer
        self.enc = tiktoken.get_encoding("gpt2")
    
    def generate(self, prompt, max_new_tokens=50, temperature=0.8, top_k=200):
        """Generate a response from a prompt"""
        start_ids = self.enc.encode_ordinary(prompt) # Convert text prompt into a list of integers
        x = torch.tensor(start_ids, dtype=torch.long, device=self.device)[None, ...] # Wrap in PyTorch tensor
        
        # Generate
        with torch.no_grad():
            with self.ctx:
                y = self.model.generate(x, max_new_tokens, temperature=temperature, top_k=top_k)
                response = self.enc.decode(y[0].tolist())
        
        # Remove the prompt from response
        return response[len(prompt):].strip()