---
name: homelab-ops
description: Work on the user's homelab machines (Linux boxes, media server, remote agents) — SSH in, troubleshoot, and check the vault's known-fix notes BEFORE diagnosing from scratch. Use for any "ssh into my box", omarchy, ZFS, Plex/SMB, clawdbot/openclaw, or black-screen/wifi issue.
---

# Homelab Ops

Homelab issues recur (omarchy black screen has happened 3+ times). The fixes are already written down — **read them first, don't re-diagnose from scratch.**

## Step 0 — always
Read the relevant note in `<vault>/Homelab/` before touching the machine:
- `Homelab.md` — machine inventory, IPs, roles (source of truth; update it when things change).
- `tooling-environment-facts.md` — environment facts.
- `project_omarchy_blackscreen.md`, `project_omarchy_wifi_wedged.md`, `project_omarchy_hyprlock.md`, etc. — known issues with the fix that actually worked.

## Known machines (verify against Homelab.md — it wins if they differ)
- **omarchy box**: `<user>@<omarchy-host>` (see Homelab.md for the address) — Arch/Hyprland (Omarchy), recurring black-screen/SDDM/UWSM and iwd wifi issues.
- **media server**: Plex + ZFS pool + SMB.
- Other boxes/IPs: see `Homelab.md`.

## Rules
1. **Check config files and unit ordering before guessing root causes** (systemd, `.zshrc`/`.bashrc`, mise, iwd) — evidence over assumption.
2. After fixing something, **write the fix back** to the matching `project_*.md` note (or create one) so next time starts from the answer. Update, don't duplicate.
3. For services: after any change verify the service actually survives a reboot (`systemctl is-enabled`, fstab/zfs mount units) — the user always wants persistence, not a one-time fix.
4. If SSH is unreachable, suggest checks the user can do at the console (tty login, `systemctl restart iwd`, SDDM session choice: Hyprland not UWSM) rather than retrying blindly.

---
Created by Claude Fable 5 on 2026-07-04 09:03 PT
