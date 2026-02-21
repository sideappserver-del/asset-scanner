import tkinter as tk
from tkinter import ttk, messagebox
import os
from pathlib import Path
import threading
from datetime import datetime
import re

class AssetScanner:
    def __init__(self, root):
        self.root = root
        self.root.title('Asset Scanner')
        self.root.geometry('950x800')
        self.root.resizable(False, False)
        
        # Colors: Gold and Black theme
        self.bg_color = '#1a1a1a'  # Black
        self.gold_color = '#FFD700'  # Gold
        self.text_color = '#FFFFFF'  # White text
        self.dark_gold = '#DAA520'  # Darker gold
        self.alert_color = '#FF6B6B'  # Red for alerts
        self.success_color = '#51CF66'  # Green for success
        self.warning_color = '#FFD93D'  # Yellow for warnings
        
        self.root.configure(bg=self.bg_color)
        self.scanning = False
        self.found_files = {}
        
        # Top frame with logo and title
        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(pady=10)
        
        # Create a simple coin logo using canvas
        logo_canvas = tk.Canvas(top_frame, width=60, height=60, bg=self.bg_color, highlightthickness=0)
        logo_canvas.pack(side=tk.LEFT, padx=(20, 15))
        
        # Draw a gold coin
        # Outer circle (coin edge)
        logo_canvas.create_oval(5, 5, 55, 55, outline=self.gold_color, width=3)
        # Inner circle (coin face)
        logo_canvas.create_oval(10, 10, 50, 50, fill=self.gold_color, outline=self.dark_gold, width=2)
        # Dollar sign in center
        logo_canvas.create_text(30, 32, text='$', font=('Arial', 32, 'bold'), fill=self.bg_color)
        
        # Title and subtitle frame
        title_frame = tk.Frame(top_frame, bg=self.bg_color)
        title_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(
            title_frame,
            text='ASSET SCANNER',
            font=('Arial', 22, 'bold'),
            bg=self.bg_color,
            fg=self.gold_color
        )
        title.pack(anchor='w')
        
        # Subtitle
        subtitle = tk.Label(
            title_frame,
            text='Discover Hidden Cryptocurrency & Digital Assets',
            font=('Arial', 10),
            bg=self.bg_color,
            fg=self.text_color
        )
        subtitle.pack(anchor='w', pady=(2, 0))
        
        # Control frame - Scan button
        control_frame = tk.Frame(self.root, bg=self.bg_color)
        control_frame.pack(pady=(5, 12))
        
        # Big SCAN button
        self.scan_button = tk.Button(
            control_frame,
            text='SCAN FOR ASSETS',
            font=('Arial', 14, 'bold'),
            bg=self.gold_color,
            fg='#000000',
            command=self.start_scan,
            padx=30,
            pady=10,
            cursor='hand2'
        )
        self.scan_button.pack(side=tk.LEFT, padx=10)
        
        # Main content frame - three columns
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))
        
        # LEFT COLUMN - Results
        left_frame = tk.Frame(main_frame, bg=self.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        results_label = tk.Label(
            left_frame,
            text='SCAN RESULTS:',
            font=('Arial', 9, 'bold'),
            bg=self.bg_color,
            fg=self.gold_color
        )
        results_label.pack(anchor='w', pady=(0, 5))
        
        # Results text area
        self.results_text = tk.Text(
            left_frame,
            height=24,
            width=40,
            bg='#2a2a2a',
            fg=self.text_color,
            font=('Courier', 7),
            insertbackground=self.gold_color
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # CENTER COLUMN - File Details
        center_frame = tk.Frame(main_frame, bg=self.bg_color)
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        details_label = tk.Label(
            center_frame,
            text='FILE DETAILS:',
            font=('Arial', 9, 'bold'),
            bg=self.bg_color,
            fg=self.gold_color
        )
        details_label.pack(anchor='w', pady=(0, 5))
        
        # File details text area
        self.details_text = tk.Text(
            center_frame,
            height=24,
            width=40,
            bg='#2a2a2a',
            fg=self.text_color,
            font=('Courier', 7),
            insertbackground=self.gold_color
        )
        self.details_text.pack(fill=tk.BOTH, expand=True)
        self.details_text.insert(tk.END, 'Click a file in Results\nto see details here.')
        self.details_text.config(state='disabled')
        
        # RIGHT COLUMN - Solutions
        right_frame = tk.Frame(main_frame, bg=self.bg_color)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        solutions_label = tk.Label(
            right_frame,
            text='SECURITY SOLUTIONS:',
            font=('Arial', 9, 'bold'),
            bg=self.bg_color,
            fg=self.gold_color
        )
        solutions_label.pack(anchor='w', pady=(0, 5))
        
        # Solutions text area
        self.solutions_text = tk.Text(
            right_frame,
            height=24,
            width=40,
            bg='#2a2a2a',
            fg=self.text_color,
            font=('Courier', 7),
            insertbackground=self.gold_color
        )
        self.solutions_text.pack(fill=tk.BOTH, expand=True)
        self.solutions_text.insert(tk.END, 'Select file details\nto see solutions.')
        self.solutions_text.config(state='disabled')
        
        # Bind click event to results
        self.results_text.bind('<Button-1>', self.on_result_click)
        
        # Bottom buttons frame
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=(0, 8))
        
        # Info button
        info_button = tk.Button(
            button_frame,
            text='How This Works',
            font=('Arial', 9),
            bg=self.dark_gold,
            fg='#000000',
            command=self.show_info,
            padx=12,
            pady=6,
            cursor='hand2'
        )
        info_button.pack(side=tk.LEFT, padx=8)
        
        # FAQ Button
        faq_button = tk.Button(
            button_frame,
            text='False Positives?',
            font=('Arial', 9),
            bg=self.dark_gold,
            fg='#000000',
            command=self.show_faq,
            padx=12,
            pady=6,
            cursor='hand2'
        )
        faq_button.pack(side=tk.LEFT, padx=8)
        
        # Clear button
        clear_button = tk.Button(
            button_frame,
            text='Clear Results',
            font=('Arial', 9),
            bg=self.dark_gold,
            fg='#000000',
            command=self.clear_results,
            padx=12,
            pady=6,
            cursor='hand2'
        )
        clear_button.pack(side=tk.LEFT, padx=8)
        
        # Exit button
        exit_button = tk.Button(
            button_frame,
            text='Exit',
            font=('Arial', 9),
            bg='#555555',
            fg=self.text_color,
            command=self.root.quit,
            padx=12,
            pady=6,
            cursor='hand2'
        )
        exit_button.pack(side=tk.LEFT, padx=8)
        
        # Footer with credits
        footer_frame = tk.Frame(self.root, bg='#0d0d0d', height=30)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        credit_label = tk.Label(
            footer_frame,
            text='Asset Scanner - Designed by R. Auel with expert assistance from GitHub Copilot',
            font=('Arial', 8),
            bg='#0d0d0d',
            fg='#888888'
        )
        credit_label.pack(pady=5)
        
        self.current_selected_file = None
    
    def analyze_file(self, file_path, category):
        """Analyze file to determine if it's likely a real wallet"""
        analysis = {
            'path': file_path,
            'category': category,
            'risk_level': 'LOW',
            'confidence': 0,
            'value_estimate': 'UNKNOWN',
            'reasons': [],
            'false_positive_risk': []
        }
        
        try:
            # Get file stats
            file_stat = os.stat(file_path)
            file_size = file_stat.st_size
            mod_time = datetime.fromtimestamp(file_stat.st_mtime)
            days_old = (datetime.now() - mod_time).days
            
            # Check file size
            if file_size == 0:
                analysis['false_positive_risk'].append('Empty file - likely not a real wallet')
                analysis['confidence'] = 5
            elif file_size < 100:
                analysis['false_positive_risk'].append('Very small file - might be placeholder/config')
                analysis['confidence'] = 30
            elif file_size > 100 and file_size < 10000000:
                analysis['reasons'].append(f'Normal wallet file size: {file_size} bytes')
                analysis['confidence'] += 40
            
            # Check modification date
            if days_old < 7:
                analysis['reasons'].append(f'Recently modified ({days_old} days ago) - actively used')
                analysis['confidence'] += 30
                analysis['risk_level'] = 'HIGH'
            elif days_old < 365:
                analysis['reasons'].append(f'Modified {days_old} days ago - may be active')
                analysis['confidence'] += 20
                analysis['risk_level'] = 'MEDIUM'
            elif days_old > 1095:
                analysis['false_positive_risk'].append(f'Not modified in {days_old} days - may be abandoned/test file')
                analysis['confidence'] = max(analysis['confidence'] - 15, 0)
            
            # Category-specific analysis
            if category == 'Bitcoin':
                if 'wallet.dat' in file_path.lower():
                    if file_size > 1000:
                        analysis['reasons'].append('Bitcoin Core wallet.dat detected')
                        analysis['confidence'] += 20
            
            elif category == 'Ethereum':
                if 'UTC--' in file_path or 'keystore' in file_path:
                    if file_size > 100 and file_size < 100000:
                        analysis['reasons'].append('Ethereum keystore file size matches real wallet')
                        analysis['confidence'] += 20
            
            elif category == 'Seed Phrases':
                if '.txt' in file_path.lower():
                    try:
                        with open(file_path, 'r', errors='ignore') as f:
                            content = f.read()
                            word_count = len(content.split())
                            if 12 <= word_count <= 24:
                                analysis['reasons'].append('File contains ~12-24 words (BIP39 seed format)')
                                analysis['confidence'] += 25
                                analysis['risk_level'] = 'HIGH'
                            elif word_count < 5:
                                analysis['false_positive_risk'].append('Only a few words - unlikely seed phrase')
                    except:
                        pass
            
            # Risk assessment
            if analysis['confidence'] >= 70:
                analysis['risk_level'] = 'HIGH'
                analysis['value_estimate'] = 'POTENTIALLY VALUABLE'
            elif analysis['confidence'] >= 40:
                analysis['risk_level'] = 'MEDIUM'
                analysis['value_estimate'] = 'UNKNOWN'
            else:
                analysis['risk_level'] = 'LOW'
                analysis['value_estimate'] = 'LIKELY FALSE POSITIVE'
            
        except Exception as e:
            analysis['false_positive_risk'].append(f'Error analyzing: {str(e)}')
        
        return analysis
    
    def on_result_click(self, event):
        """Handle clicks in results text to show details"""
        try:
            line_start = self.results_text.index(f"@{event.x},{event.y} linestart")
            line_end = self.results_text.index(f"@{event.x},{event.y} lineend")
            line_text = self.results_text.get(line_start, line_end).strip()
            
            # Try to find this file in our found_files
            for category, files in self.found_files.items():
                for file_info in files:
                    if file_info['path'] in line_text or line_text.endswith(file_info['path'].split('\\')[-1]):
                        self.show_file_details(file_info, category)
                        return
        except:
            pass
    
    def show_file_details(self, file_info, category):
        """Show detailed analysis of a selected file"""
        file_path = file_info['path']
        analysis = file_info.get('analysis', {})
        
        self.details_text.config(state='normal')
        self.details_text.delete(1.0, tk.END)
        
        self.details_text.insert(tk.END, f"FILE: {file_path.split(chr(92))[-1]}\n")
        self.details_text.insert(tk.END, '=' * 38 + '\n\n')
        
        self.details_text.insert(tk.END, f"Category: {category}\n")
        self.details_text.insert(tk.END, f"Risk Level: {analysis.get('risk_level', 'UNKNOWN')}\n")
        self.details_text.insert(tk.END, f"Confidence: {analysis.get('confidence', 0)}%\n")
        self.details_text.insert(tk.END, f"Value: {analysis.get('value_estimate', 'UNKNOWN')}\n\n")
        
        if analysis.get('reasons'):
            self.details_text.insert(tk.END, "POSITIVE INDICATORS:\n")
            for reason in analysis.get('reasons', []):
                self.details_text.insert(tk.END, f"  + {reason}\n")
            self.details_text.insert(tk.END, "\n")
        
        if analysis.get('false_positive_risk'):
            self.details_text.insert(tk.END, "CAUTIONS:\n")
            for risk in analysis.get('false_positive_risk', []):
                self.details_text.insert(tk.END, f"  ! {risk}\n")
            self.details_text.insert(tk.END, "\n")
        
        self.details_text.insert(tk.END, f"Path:\n{file_path}\n")
        
        self.details_text.config(state='disabled')
        
        # Show solutions for this category
        self.show_solutions_for_category(category)
        self.current_selected_file = file_info
    
    def show_solutions_for_category(self, category):
        """Show security solutions for asset type"""
        solutions = {
            'Bitcoin': """BITCOIN WALLET SECURITY

IMMEDIATE ACTIONS:
1. Verify this is YOUR wallet
   - Check file creation/modification date
   - Confirm it belongs to your wallet

2. Back it up securely
   - Copy to encrypted USB drive
   - Store in physically secure location

3. Check the blockchain
   - Google the wallet address if known
   - Verify balance on blockchain explorer

4. Enable security
   - Add password protection if needed
   - Consider hardware wallet

5. Monitor regularly
   - Check for unauthorized activity
   - Review transaction history""",

            'Ethereum': """ETHEREUM WALLET SECURITY

IMMEDIATE ACTIONS:
1. Verify ownership
   - Check wallet on Etherscan.io
   - Confirm all transactions are yours
   - Check current balance

2. Secure the backup
   - Move keystore to encrypted drive
   - Store password separately
   - Use strong password

3. Check for tokens
   - Go to Etherscan.io wallet page
   - View all ERC-20 tokens
   - Note values and amounts

4. Move to safety
   - Consider hardware wallet
   - Withdraw to secure address
   - Enable 2FA on exchanges

5. Protect going forward
   - Set up transaction alerts
   - Monitor wallet regularly
   - Never share private keys""",

            'Wallet Backups': """WALLET BACKUP SECURITY

IMMEDIATE ACTIONS:
1. Identify wallet type
   - Check file extension
   - Look for comments/metadata
   - Research the app

2. Secure immediately
   - Move to encrypted drive
   - Delete from original location
   - Use secure deletion

3. Access the wallet
   - Check balance online if possible
   - Verify you have correct password
   - Test on small transaction

4. Protect the backup
   - Encrypt with strong password
   - Store in secure location
   - Consider printed backup

5. Recovery plan
   - Write down location
   - Store password securely
   - Test restore process""",

            'Seed Phrases': """SEED PHRASE SECURITY (CRITICAL!)

WARNING: SEED PHRASE = FULL WALLET ACCESS!

IMMEDIATE ACTIONS:
1. NEVER type this into computer again
   - Delete this file immediately
   - Should only exist on paper
   - Delete digital copy now

2. Move to secure backup
   - Write on paper (laminate)
   - Store in safe deposit box
   - Multiple copies, different locations

3. Delete digital copy
   - Use secure deletion
   - Empty trash permanently
   - Wipe free space

4. Test your access
   - Use seed to restore wallet
   - Verify all funds present
   - Move to hardware wallet

5. NEVER SHARE THIS
   - Not with family
   - Not in emails
   - Not in cloud storage
   - Not in screenshots

CRITICAL: Anyone with seed phrase 
OWNS THE WALLET!""",

            'MetaMask': """METAMASK WALLET SECURITY

IMMEDIATE ACTIONS:
1. Check your MetaMask
   - Open Chrome/Firefox extension
   - Review recent transactions
   - Check all account balances

2. Backup security
   - Seed phrase should NOT be on disk
   - Move to paper/secure backup
   - Keep password protected

3. Review connected sites
   - Open Settings > Connected Sites
   - Remove unused dApps
   - Revoke token approvals

4. Enable security
   - Set strong password
   - Enable browser lock
   - Update MetaMask

5. Protect the backup
   - Seed on paper only
   - Delete this file
   - Use secure deletion

WARNING: Anyone with this file 
can drain your MetaMask accounts!""",

            'Ledger': """HARDWARE WALLET SECURITY

IMMEDIATE ACTIONS:
1. Verify your device
   - Connect physical Ledger
   - Open Ledger Live
   - Confirm accounts visible

2. Update Ledger
   - Run latest Ledger Live
   - Check firmware updates
   - Update hardware device

3. Secure the backup
   - Seed phrase on paper only
   - Config file is okay on device
   - Enable PIN on Ledger

4. Review accounts
   - Check all wallets
   - Verify transactions
   - Monitor for unauthorized access

5. Ongoing security
   - Always verify address on device
   - Never share seed phrase
   - Update regularly
   - Use official Ledger only""",

            'Electrum': """ELECTRUM WALLET SECURITY

IMMEDIATE ACTIONS:
1. Launch Electrum
   - Open application
   - Go to File > Open Recent
   - Verify password works

2. Check wallet status
   - View balance
   - Check transactions
   - Verify seed phrase

3. Backup security
   - Seed phrase on paper
   - Wallet file encrypted
   - Keep offline storage

4. Update Electrum
   - Check for latest version
   - Download from official site only
   - Verify signature if possible

5. Secure the wallet
   - Encrypt with strong password
   - Enable 2FA on exchanges
   - Consider hardware wallet

NOTE: Always download from 
electrum.org only!""",

            'Mining': """MINING CONFIGURATION SECURITY

IMMEDIATE ACTIONS:
1. Check for wallet addresses
   - Open config file
   - Extract wallet addresses
   - Check balance on blockchain

2. Check pool accounts
   - Log into pool account
   - Verify recent payouts
   - Update password

3. Secure credentials
   - Change pool passwords
   - Update wallet address
   - Review API keys

4. Recover payouts
   - Check unpaid balance
   - Withdraw to secure wallet
   - Verify confirmations

5. Protect configuration
   - Store securely
   - Backup API keys
   - Encrypt files
   - Remove from public folders""",

            'Default': """GENERAL ASSET SECURITY

IMMEDIATE ACTIONS:
1. Identify the asset
   - Research file type
   - Check properties
   - Verify ownership

2. Check current status
   - Search blockchain
   - Check balance
   - Review history

3. Secure the file
   - Move to encrypted storage
   - Use strong password
   - Delete original

4. Protect access
   - Use encrypted drives
   - Enable full disk encryption
   - Limit access

5. Plan next steps
   - Decide on hardware wallet
   - Set monitoring alerts
   - Document location"""
        }
        
        sol_text = solutions.get(category, solutions['Default'])
        
        self.solutions_text.config(state='normal')
        self.solutions_text.delete(1.0, tk.END)
        self.solutions_text.insert(tk.END, sol_text)
        self.solutions_text.config(state='disabled')
    
    def show_faq(self):
        """Show False Positive FAQ"""
        faq_text = """FALSE POSITIVES FAQ

WHAT IS A FALSE POSITIVE?
A "false positive" is when the scanner finds a file 
that LOOKS like a cryptocurrency wallet but isn't 
really one with actual value.

EXAMPLES OF FALSE POSITIVES:
- wallet.dat from a video game
- "ethereum" in a folder name you created
- seed.txt with gardening notes
- mining.conf from 5 years ago (long abandoned)
- GitHub downloads with "bitcoin" in comments
- Test files or old backups with no funds

WHY DOES THIS HAPPEN?
The scanner looks for file names and patterns, not 
actual wallet data. This is necessary because:
- Real wallets use standard file names
- Can't open/decrypt files without permission
- Can't always contact blockchain to check balance

HOW TO FILTER FALSE POSITIVES:
Look at the categorization:
- "LIKELY HAS VALUE" = High confidence (70%+)
- "POSSIBLY HAS VALUE" = Medium confidence (40-70%)
- "LIKELY NOT VALUE" = Low confidence (<40%)

WHAT TO DO WITH SUSPECTS:
1. Check the file modification date
   - Recent = likely real
   - Very old = likely abandoned/test

2. Check the file size
   - Empty/tiny = likely false positive
   - Large = likely real wallet

3. Check the path
   - In Documents/Downloads = likely real
   - In temporary/game folders = likely false

4. Try to verify
   - Can you remember creating this?
   - Does it have a wallet address?
   - Is it password protected?

5. When in doubt
   - Move to secure backup
   - Keep encrypted
   - Research the file type
   - Check blockchain if you have address

BOTTOM LINE:
Check the confidence percentage! Low confidence 
files are probably not real wallets with funds!"""
        
        messagebox.showinfo('False Positives Explained', faq_text)
    
    def start_scan(self):
        """Start scan in background thread"""
        if self.scanning:
            return
        
        self.scanning = True
        self.scan_button.config(state='disabled', text='SCANNING...')
        self.results_text.delete(1.0, tk.END)
        self.clear_results()
        
        scan_thread = threading.Thread(target=self.perform_scan, daemon=True)
        scan_thread.start()
    
    def perform_scan(self):
        """Search for crypto wallet files with analysis"""
        self.results_text.insert(tk.END, 'Scanning for cryptocurrency assets...\n')
        self.results_text.insert(tk.END, '=' * 45 + '\n\n')
        self.root.update()
        
        search_patterns = {
            'Bitcoin': ['wallet.dat', 'bitcoin.conf'],
            'Ethereum': ['keystore', 'UTC--', 'ethereum'],
            'Wallet Backups': ['.wallet', '.key', '.pem', '.priv'],
            'Seed Phrases': ['seed.txt', 'mnemonic.txt', 'recovery.txt', 'phrase'],
            'MetaMask': ['chrome-extension', 'metamask'],
            'Ledger': ['ledger', 'hw-app', 'ledger_live'],
            'Electrum': ['electrum_data', '.electrum', 'electrum'],
            'Mining': ['mining', 'miner.conf', '.bat'],
        }
        
        home = str(Path.home())
        search_folders = [
            os.path.join(home, 'Documents'),
            os.path.join(home, 'Downloads'),
            os.path.join(home, 'Desktop'),
            os.path.join(home, 'AppData', 'Roaming'),
            os.path.join(home, 'AppData', 'Local'),
        ]
        
        self.found_files = {}
        scanned_count = 0
        
        for folder in search_folders:
            if not os.path.exists(folder):
                continue
            
            self.results_text.insert(tk.END, f'Searching: {folder}\n')
            self.root.update()
            
            try:
                for root_dir, dirs, files in os.walk(folder):
                    dirs[:] = [d for d in dirs if d not in ['System Volume Information', '$RECYCLE.BIN']]
                    
                    for file in files:
                        scanned_count += 1
                        file_lower = file.lower()
                        
                        for category, patterns in search_patterns.items():
                            for pattern in patterns:
                                if pattern.lower() in file_lower:
                                    file_path = os.path.join(root_dir, file)
                                    
                                    if category not in self.found_files:
                                        self.found_files[category] = []
                                    
                                    try:
                                        file_size = os.path.getsize(file_path)
                                        
                                        # Analyze the file
                                        analysis = self.analyze_file(file_path, category)
                                        
                                        self.found_files[category].append({
                                            'path': file_path,
                                            'size': file_size,
                                            'pattern': pattern,
                                            'analysis': analysis
                                        })
                                    except:
                                        pass
                                    break
            except PermissionError:
                continue
            except Exception as e:
                continue
        
        # Now display results categorized by likelihood
        self.display_results_by_likelihood(scanned_count)
        
        self.scanning = False
        self.scan_button.config(state='normal', text='SCAN FOR ASSETS')
        self.root.update()
    
    def display_results_by_likelihood(self, scanned_count):
        """Display results categorized by likelihood of being real"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, 'SCAN RESULTS:\n')
        self.results_text.insert(tk.END, '=' * 45 + '\n\n')
        
        if not self.found_files:
            self.results_text.insert(tk.END, 'No files found.\n')
            self.results_text.insert(tk.END, '=' * 45 + '\n')
            self.results_text.insert(tk.END, f'Scan complete!\nScanned: {scanned_count} files\n')
            return
        
        # Categorize files by confidence
        likely_money = []      # 70%+ confidence
        possibly_money = []    # 40-70% confidence
        likely_not = []        # <40% confidence
        
        for category, files in self.found_files.items():
            for f in files:
                confidence = f['analysis'].get('confidence', 0)
                if confidence >= 70:
                    likely_money.append((category, f))
                elif confidence >= 40:
                    possibly_money.append((category, f))
                else:
                    likely_not.append((category, f))
        
        # Display LIKELY MONEY section
        if likely_money:
            self.results_text.insert(tk.END, '*** LIKELY HAS VALUE ***\n')
            self.results_text.insert(tk.END, '-' * 45 + '\n')
            
            category_groups = {}
            for category, f in likely_money:
                if category not in category_groups:
                    category_groups[category] = []
                category_groups[category].append(f)
            
            for category in sorted(category_groups.keys()):
                files = category_groups[category]
                self.results_text.insert(tk.END, f'\n[{category}] {len(files)} file(s)\n')
                
                for f in files[:2]:
                    filename = f['path'].split('\\')[-1]
                    confidence = f['analysis'].get('confidence', 0)
                    self.results_text.insert(tk.END, f'  {filename}\n')
                    self.results_text.insert(tk.END, f'  (Confidence: {confidence}%)\n')
                
                if len(files) > 2:
                    self.results_text.insert(tk.END, f'  ... +{len(files)-2} more\n')
            
            self.results_text.insert(tk.END, '\n' + '=' * 45 + '\n\n')
        
        # Display POSSIBLY MONEY section
        if possibly_money:
            self.results_text.insert(tk.END, '? POSSIBLY HAS VALUE ?\n')
            self.results_text.insert(tk.END, '-' * 45 + '\n')
            
            category_groups = {}
            for category, f in possibly_money:
                if category not in category_groups:
                    category_groups[category] = []
                category_groups[category].append(f)
            
            for category in sorted(category_groups.keys()):
                files = category_groups[category]
                self.results_text.insert(tk.END, f'\n[{category}] {len(files)} file(s)\n')
                
                for f in files[:2]:
                    filename = f['path'].split('\\')[-1]
                    confidence = f['analysis'].get('confidence', 0)
                    self.results_text.insert(tk.END, f'  {filename}\n')
                    self.results_text.insert(tk.END, f'  (Confidence: {confidence}%)\n')
                
                if len(files) > 2:
                    self.results_text.insert(tk.END, f'  ... +{len(files)-2} more\n')
            
            self.results_text.insert(tk.END, '\n' + '=' * 45 + '\n\n')
        
        # Display LIKELY NOT section
        if likely_not:
            self.results_text.insert(tk.END, 'o LIKELY NOT VALUE o\n')
            self.results_text.insert(tk.END, '-' * 45 + '\n')
            
            category_groups = {}
            for category, f in likely_not:
                if category not in category_groups:
                    category_groups[category] = []
                category_groups[category].append(f)
            
            for category in sorted(category_groups.keys()):
                files = category_groups[category]
                self.results_text.insert(tk.END, f'\n[{category}] {len(files)} file(s)\n')
                
                for f in files[:1]:
                    filename = f['path'].split('\\')[-1]
                    confidence = f['analysis'].get('confidence', 0)
                    self.results_text.insert(tk.END, f'  {filename}\n')
                    self.results_text.insert(tk.END, f'  (Confidence: {confidence}%)\n')
                
                if len(files) > 1:
                    self.results_text.insert(tk.END, f'  ... +{len(files)-1} more\n')
            
            self.results_text.insert(tk.END, '\n' + '=' * 45 + '\n\n')
        
        # Summary
        self.results_text.insert(tk.END, 'SUMMARY:\n')
        self.results_text.insert(tk.END, f'Likely Money: {len(likely_money)}\n')
        self.results_text.insert(tk.END, f'Possibly Money: {len(possibly_money)}\n')
        self.results_text.insert(tk.END, f'Likely Not: {len(likely_not)}\n\n')
        self.results_text.insert(tk.END, f'Scanned: {scanned_count} files\n\n')
        self.results_text.insert(tk.END, 'Click file to see\nanalysis & solutions')
    
    def show_info(self):
        """Show How This Works info"""
        info_text = """ASSET SCANNER - How This Works

WHAT IT DOES:
Scans your computer for cryptocurrency wallets
and digital assets you may have forgotten about.

CONFIDENCE LEVELS:
*** LIKELY HAS VALUE *** (70%+)
- Recently modified
- Proper file size
- Strong real wallet indicators

? POSSIBLY HAS VALUE ? (40-70%)
- Moderate confidence indicators
- May need verification
- Could be real or false positive

o LIKELY NOT VALUE o (<40%)
- Old file date
- Wrong file size
- Missing wallet indicators
- Possible false positive

YOUR SECURITY:
[YES] NO INTERNET - 100% local
[YES] NO DATA SENT - Nothing uploaded
[YES] NO LOGS - Deleted after close
[YES] NO PERMISSIONS - Camera/location OFF

WHERE IT SEARCHES:
- Documents
- Downloads
- Desktop
- AppData folders
- User directory

WHAT TO DO:
1. Run scan
2. Review results by likelihood
3. Click file for full analysis
4. Follow security steps
5. Secure your assets

DISCLAIMER:
Verify files are actually yours 
before taking any action!"""
        messagebox.showinfo('How This Works', info_text)
    
    def clear_results(self):
        """Clear all displays"""
        self.results_text.delete(1.0, tk.END)
        self.details_text.config(state='normal')
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, 'Click a file in Results\nto see details here.')
        self.details_text.config(state='disabled')
        self.solutions_text.config(state='normal')
        self.solutions_text.delete(1.0, tk.END)
        self.solutions_text.insert(tk.END, 'Select file details\nto see solutions.')
        self.solutions_text.config(state='disabled')

# Run the app
if __name__ == '__main__':
    root = tk.Tk()
    app = AssetScanner(root)
    root.mainloop()