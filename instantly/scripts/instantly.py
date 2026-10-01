#!/usr/bin/env python3
"""
Instantly.ai CLI wrapper for common operations.

Usage:
    python instantly.py campaigns list
    python instantly.py campaigns get <id>
    python instantly.py campaigns activate <id>
    python instantly.py campaigns pause <id>
    
    python instantly.py leads list --campaign <id> [--limit 100]
    python instantly.py leads add --campaign <id> --email <email> [--first <name>] [--last <name>]
    python instantly.py leads import --campaign <id> --csv <file.csv>
    
    python instantly.py accounts list
    python instantly.py accounts warmup-enable <email>
    python instantly.py accounts warmup-disable <email>
    
    python instantly.py analytics --campaign <id>
    python instantly.py unread
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path

import requests

API_BASE = "https://api.instantly.ai/api/v2"
KEY_PATH = Path.home() / ".config/instantly/api_key.txt"


def get_api_key():
    if KEY_PATH.exists():
        return KEY_PATH.read_text().strip()
    key = os.environ.get("INSTANTLY_API_KEY")
    if key:
        return key
    print(f"Error: No API key found. Set INSTANTLY_API_KEY or save to {KEY_PATH}")
    sys.exit(1)


def api(method, endpoint, data=None, params=None):
    """Make API request."""
    url = f"{API_BASE}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/json"
    }
    
    if method == "GET":
        resp = requests.get(url, headers=headers, params=params)
    elif method == "POST":
        resp = requests.post(url, headers=headers, json=data, params=params)
    elif method == "PATCH":
        resp = requests.patch(url, headers=headers, json=data)
    elif method == "DELETE":
        resp = requests.delete(url, headers=headers)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    if resp.status_code >= 400:
        print(f"Error {resp.status_code}: {resp.text}")
        sys.exit(1)
    
    return resp.json() if resp.text else {}


def cmd_campaigns(args):
    if args.action == "list":
        result = api("GET", "campaigns")
        for c in result.get("items", []):
            status = c.get("status", "unknown")
            print(f"{c['id']}: {c['name']} [{status}]")
    
    elif args.action == "get":
        result = api("GET", f"campaigns/{args.id}")
        print(json.dumps(result, indent=2))
    
    elif args.action == "activate":
        api("POST", f"campaigns/{args.id}/activate")
        print(f"Campaign {args.id} activated")
    
    elif args.action == "pause":
        api("POST", f"campaigns/{args.id}/pause")
        print(f"Campaign {args.id} paused")


def cmd_leads(args):
    if args.action == "list":
        data = {"campaign_id": args.campaign, "limit": args.limit or 100}
        result = api("POST", "leads/list", data)
        for lead in result.get("items", []):
            email = lead.get("email", "")
            status = lead.get("interest_status", "")
            print(f"{lead['id']}: {email} [{status}]")
    
    elif args.action == "add":
        data = {
            "campaign_id": args.campaign,
            "email": args.email,
        }
        if args.first:
            data["first_name"] = args.first
        if args.last:
            data["last_name"] = args.last
        if args.company:
            data["company_name"] = args.company
        
        result = api("POST", "leads", data)
        print(f"Added: {result.get('id', 'ok')}")
    
    elif args.action == "import":
        if not args.csv:
            print("Error: --csv required for import")
            sys.exit(1)
        
        leads = []
        with open(args.csv, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                lead = {"email": row.get("email") or row.get("Email") or row.get("Email Address")}
                if not lead["email"]:
                    continue
                
                # Map common field names
                for src, dst in [
                    (["first_name", "First Name", "FirstName", "first"], "first_name"),
                    (["last_name", "Last Name", "LastName", "last"], "last_name"),
                    (["company", "Company", "company_name", "Company Name"], "company_name"),
                ]:
                    for s in src:
                        if s in row and row[s]:
                            lead[dst] = row[s]
                            break
                
                # Add remaining fields as custom variables
                custom = {}
                skip = {"email", "Email", "Email Address", "first_name", "last_name", 
                        "company_name", "First Name", "Last Name", "Company", "Company Name",
                        "first", "last", "FirstName", "LastName"}
                for k, v in row.items():
                    if k not in skip and v:
                        custom[k] = v
                if custom:
                    lead["custom_variables"] = custom
                
                leads.append(lead)
        
        print(f"Importing {len(leads)} leads to campaign {args.campaign}...")
        
        # Batch in chunks of 100
        for i in range(0, len(leads), 100):
            batch = leads[i:i+100]
            api("POST", "leads/batch", {"campaign_id": args.campaign, "leads": batch})
            print(f"  Imported {min(i+100, len(leads))}/{len(leads)}")
        
        print("Done!")


def cmd_accounts(args):
    if args.action == "list":
        result = api("GET", "accounts")
        for acc in result.get("items", []):
            email = acc.get("email", "")
            status = acc.get("status", "")
            warmup = "warmup" if acc.get("warmup_enabled") else ""
            print(f"{email} [{status}] {warmup}")
    
    elif args.action == "warmup-enable":
        api("POST", "accounts/warmup/enable", {"emails": [args.email]})
        print(f"Warmup enabled for {args.email}")
    
    elif args.action == "warmup-disable":
        api("POST", "accounts/warmup/disable", {"emails": [args.email]})
        print(f"Warmup disabled for {args.email}")


def cmd_analytics(args):
    params = {}
    if args.campaign:
        params["id"] = args.campaign
    
    result = api("GET", "campaigns/analytics", params=params)
    print(json.dumps(result, indent=2))


def cmd_unread(args):
    result = api("GET", "emails/unread/count")
    print(f"Unread: {result.get('count', 0)}")


def main():
    parser = argparse.ArgumentParser(description="Instantly.ai CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    # Campaigns
    p_camp = subparsers.add_parser("campaigns")
    p_camp.add_argument("action", choices=["list", "get", "activate", "pause"])
    p_camp.add_argument("id", nargs="?")
    
    # Leads
    p_leads = subparsers.add_parser("leads")
    p_leads.add_argument("action", choices=["list", "add", "import"])
    p_leads.add_argument("--campaign", required=True)
    p_leads.add_argument("--email")
    p_leads.add_argument("--first")
    p_leads.add_argument("--last")
    p_leads.add_argument("--company")
    p_leads.add_argument("--csv")
    p_leads.add_argument("--limit", type=int, default=100)
    
    # Accounts
    p_acc = subparsers.add_parser("accounts")
    p_acc.add_argument("action", choices=["list", "warmup-enable", "warmup-disable"])
    p_acc.add_argument("email", nargs="?")
    
    # Analytics
    p_analytics = subparsers.add_parser("analytics")
    p_analytics.add_argument("--campaign")
    
    # Unread
    subparsers.add_parser("unread")
    
    args = parser.parse_args()
    
    if args.command == "campaigns":
        cmd_campaigns(args)
    elif args.command == "leads":
        cmd_leads(args)
    elif args.command == "accounts":
        cmd_accounts(args)
    elif args.command == "analytics":
        cmd_analytics(args)
    elif args.command == "unread":
        cmd_unread(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
