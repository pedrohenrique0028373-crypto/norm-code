import click
import os
import sys
from .core import generate, DEFAULT_MODEL

BANNER = r"""
 _   _                 _____          _      
| \ | | ___  _ __ ___ |  ___|_ _  ___| | __  
|  \| |/ _ \| '__/ _ \| |_ / _` |/ __| |/ /  
| |\  | (_) | | | (_) |  _| (_| | (__|   <   
|_| \_|\___/|_|  \___/|_|  \__,_|\___|_|\_\  
           Norm Code – criador por Cassius
"""

@click.group()
def main():
    """Norm Code – CLI para Ollama (inspirado no Claude Code)."""
    click.echo(BANNER)

@main.command()
@click.argument("prompt", nargs=-1, required=True)
@click.option("-m", "--model", default=DEFAULT_MODEL,
              help="Modelo da Ollama a ser usado.")
@click.option("-s", "--system", default=None,
              help="Prompt do sistema (instruções de alto nível).")
def ask(prompt, model, system):
    """Envia uma pergunta ao modelo e exibe a resposta."""
    text = " ".join(prompt)
    click.echo(click.style("\n📨 Prompt:", fg="cyan"))
    click.echo(text)
    click.echo(click.style("\n🤖 Resposta:", fg="green"))
    try:
        answer = generate(text, model=model, system=system)
    except Exception as e:
        click.echo(click.style(f"❌ Erro ao chamar a Ollama: {e}", fg="red"), err=True)
        sys.exit(1)

    click.echo(answer)

@main.group()
def skill():
    """Gerencia habilidades (scripts/custom commands)."""
    pass

@skill.command("list")
def skill_list():
    """Lista todas as skills disponíveis."""
    skills_dir = os.path.join(os.path.dirname(__file__), "skills")
    if not os.path.isdir(skills_dir):
        click.echo("⚠️  Nenhum diretório de skills encontrado.")
        return

    files = [f for f in os.listdir(skills_dir) if f.endswith(".py") and f != "__init__.py"]
    if not files:
        click.echo("🔎 Nenhuma skill encontrada.")
        return

    click.echo("🛠️  Skills disponíveis:")
    for f in files:
        click.echo(f"   • {f[:-3]}")

@skill.command("run")
@click.argument("name")
@click.argument("args", nargs=-1)
def skill_run(name, args):
    """Executa uma skill, passando argumentos livres."""
    import importlib.util, pathlib

    skill_path = pathlib.Path(__file__).parent / "skills" / f"{name}.py"
    if not skill_path.is_file():
        click.echo(click.style(f"❌ Skill '{name}' não encontrada.", fg="red"))
        return

    spec = importlib.util.spec_from_file_location(name, skill_path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(mod)  # type: ignore

    if not hasattr(mod, "run"):
        click.echo(click.style("⚠️  Skill não possui função 'run'.", fg="yellow"))
        return

    try:
        result = mod.run(*args)
        click.echo(click.style("✅ Resultado:", fg="green"))
        click.echo(result)
    except Exception as exc:
        click.echo(click.style(f"❌ Erro na skill: {exc}", fg="red"))

if __name__ == "__main__":
    main()
