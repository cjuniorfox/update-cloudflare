import sqlite3
import tempfile
import logging
import os
from typing import List

class DNSRecordsRepository:
    
    def __init__(self, db_path: str | None):
        if db_path is None:
            generated_db_path = os.path.join(tempfile.gettempdir(), "update_cloudflare.db")
        self.db_path = db_path if db_path is not None and db_path != "" else generated_db_path
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialized DNSRecordsRepository with DB path: {self.db_path}")
        self._initialize_db()
        
    def _initialize_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dns_records (
                id INTEGER PRIMARY KEY,
                zone_id TEXT NOT NULL,
                dns_record_id TEXT NOT NULL,
                record_name TEXT NOT NULL,
                last_ip TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_zone_record ON dns_records (zone_id, dns_record_id, record_name)')
        conn.commit()
        conn.close()
        self.logger.info("Database initialized and ensured dns_records table exists.")
        
    def list_by(self, zone_id: str, dns_record_id: str, record_name: str) -> List[dict] | None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT zone_id, dns_record_id, record_name, last_ip, updated_at
            FROM dns_records
            WHERE zone_id = ? AND dns_record_id = ? AND record_name = ?
            ORDER BY updated_at DESC
        ''', (zone_id, dns_record_id, record_name))
        rows = cursor.fetchall()
        conn.close()
        records = []
        if rows:
            for row in rows:
                records.append({
                "zone_id": row[0],
                "dns_record_id": row[1],
                "record_name": row[2],
                "last_ip": row[3],
                "updated_at": row[4]
            })
            self.logger.debug(f"Found {len(records)} records for zone_id={zone_id}, dns_record_id={dns_record_id}, record_name={record_name}")
            return records
        else:
            self.logger.debug("No DNS records found.")
            return None
        
    def save(self, zone_id: str, dns_record_id: str, record_name: str, last_ip: str) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dns_records (zone_id, dns_record_id, record_name, last_ip)
            VALUES (?, ?, ?, ?)
        ''', (zone_id, dns_record_id, record_name, last_ip))
        conn.commit()
        conn.close()
        self.logger.info(f"Saved DNS record: zone_id={zone_id}, dns_record_id={dns_record_id}, record_name={record_name}, last_ip={last_ip}")