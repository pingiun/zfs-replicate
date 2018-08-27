"""Main function zfs-replicate."""

import itertools

import click

from .. import filesystem, snapshot, ssh, task
from ..compress import Compression
from ..filesystem import FileSystem
from ..ssh import Cipher
from .click import EnumChoice


@click.command()
@click.option("--verbose", "-v", is_flag=True, help="Print additional output.")
@click.option("--dry-run", is_flag=True, help="Generate replication tasks but do not execute them.")
@click.option(
    "--follow-delete", is_flag=True, help="Delete snapshots on REMOTE_FS that have been deleted from LOCAL_FS"
)
@click.option("--recursive", is_flag=True, help="Recursively replicate snapshots.")
@click.option("--port", "-p", type=click.IntRange(1, 65535), default=22, help="Connect to SSH on PORT.")
@click.option("--login", "-l", "--user", "-u", metavar="USER", help="Connect to SSH as USER.")
@click.option(
    "-i",
    "--identity-file",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="SSH identity file to use.",
)
@click.option(
    "--cipher",
    type=EnumChoice(Cipher),
    default=Cipher.STANDARD,
    help="""\
disabled = no ciphers
fast     = only fast ciphers
standard = default ciphers
""",
)
@click.option(
    "--compression",
    type=EnumChoice(Compression),
    default=Compression.LZ4,
    help="""\
off   = no compression
lz4   = fastest
pigz  = all rounder
plzip = best compression
""",
)
@click.argument("host", required=True, help="Replicate snapshots to HOST.")
@click.argument("remote", required=True, metavar="REMOTE_DATASET", help="Send snapshots to REMOTE_DATASET on HOST.")
@click.argument("local", required=True, metavar="LOCAL_DATASET", help="Send snapshots of LOCAL_DATASET to HOST.")
def main(  # pylint: disable=too-many-arguments,too-many-locals
    verbose: bool,
    dry_run: bool,
    follow_delete: bool,
    recursive: bool,
    port: int,
    login: str,
    identity_file: str,
    cipher: Cipher,
    compression: Compression,
    host: str,
    remote: FileSystem,
    local: FileSystem,
):
    """Main entry point into zfs-replicate."""

    ssh_command = ssh.command(cipher, login, identity_file, port, host)

    if verbose:
        click.echo(f"checking filesystem {local}")

    l_snaps = snapshot.list(local, recursive=recursive)
    # Improvment: exclusions from snapshots to replicate.

    if verbose:
        click.echo(f"found {len(l_snaps)} local snapshots")

    r_filesystem = filesystem.remote_name(remote, local)
    filesystem.create(r_filesystem, ssh_command=ssh_command)

    if verbose:
        click.echo(f"checking snapshots on {host}")

    r_snaps = snapshot.list(remote, recursive=recursive, ssh_command=ssh_command)

    import pdb

    pdb.set_trace()

    if verbose:
        click.echo(f"found {len(r_snaps)} remote snapshots")

    tasks = task.generate(l_snaps, r_snaps, follow_delete=follow_delete)

    if verbose:
        click.echo(task.report(tasks))

    if not dry_run:
        filesystem_tasks = dict(itertools.groupby(tasks, key=lambda x: x.filesystem))
        task.execute(filesystem_tasks, follow_delete=follow_delete, compression=compression, ssh_command=ssh_command)
