import requests
import hashlib
import re
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional, Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class ContentMonitor:
    """网页内容监控引擎"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def fetch_content(self, url: str, selector: Optional[str] = None) -> Optional[str]:
        """
        抓取网页内容
        
        Args:
            url: 网页URL
            selector: CSS选择器,如果指定则只提取匹配的部分
            
        Returns:
            网页内容文本,失败返回None
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            if selector:
                soup = BeautifulSoup(response.text, 'lxml')
                elements = soup.select(selector)
                if elements:
                    content = '\n'.join([elem.get_text(strip=True) for elem in elements])
                else:
                    logger.warning(f"选择器 '{selector}' 未匹配到任何元素")
                    content = response.text
            else:
                soup = BeautifulSoup(response.text, 'lxml')
                # 移除脚本和样式
                for script in soup(["script", "style"]):
                    script.decompose()
                content = soup.get_text(separator='\n', strip=True)
            
            return content
        
        except requests.RequestException as e:
            logger.error(f"抓取URL失败 {url}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"处理内容失败 {url}: {str(e)}")
            return None
    
    def calculate_hash(self, content: str) -> str:
        """
        计算内容哈希值
        
        Args:
            content: 文本内容
            
        Returns:
            SHA256哈希值
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def detect_change(self, old_hash: Optional[str], new_content: str) -> Tuple[bool, str]:
        """
        检测内容是否变化
        
        Args:
            old_hash: 旧内容的哈希值
            new_content: 新内容
            
        Returns:
            (是否变化, 新哈希值)
        """
        new_hash = self.calculate_hash(new_content)
        
        if old_hash is None:
            # 首次检查,不算变化
            return False, new_hash
        
        changed = (old_hash != new_hash)
        return changed, new_hash
    
    def extract_keywords(self, content: str, keywords: List[str]) -> List[str]:
        """
        提取匹配的关键词
        
        Args:
            content: 文本内容
            keywords: 关键词列表
            
        Returns:
            匹配到的关键词列表
        """
        if not keywords:
            return []
        
        matched = []
        content_lower = content.lower()
        
        for keyword in keywords:
            if keyword.strip():
                # 支持正则表达式
                try:
                    if re.search(keyword, content, re.IGNORECASE):
                        matched.append(keyword)
                except re.error:
                    # 如果不是有效的正则,就作为普通字符串搜索
                    if keyword.lower() in content_lower:
                        matched.append(keyword)
        
        return matched
    
    def generate_summary(self, content: str, max_length: int = 500) -> str:
        """
        生成内容摘要
        
        Args:
            content: 文本内容
            max_length: 最大长度
            
        Returns:
            摘要文本
        """
        # 移除多余的空白字符
        summary = re.sub(r'\s+', ' ', content).strip()
        
        if len(summary) > max_length:
            summary = summary[:max_length] + '...'
        
        return summary
    
    def extract_vulnerability_info(self, content: str) -> Dict[str, any]:
        """
        提取漏洞相关信息
        
        Args:
            content: 文本内容
            
        Returns:
            包含CVE编号、CVSS评分等信息的字典
        """
        info = {
            'cve_ids': [],
            'cnvd_ids': [],
            'cnnvd_ids': [],
            'cvss_scores': [],
            'severity_levels': []
        }
        
        # 提取CVE编号
        cve_pattern = r'CVE-\d{4}-\d{4,7}'
        info['cve_ids'] = list(set(re.findall(cve_pattern, content, re.IGNORECASE)))
        
        # 提取CNVD编号
        cnvd_pattern = r'CNVD-\d{4}-\d{5,6}'
        info['cnvd_ids'] = list(set(re.findall(cnvd_pattern, content, re.IGNORECASE)))
        
        # 提取CNNVD编号
        cnnvd_pattern = r'CNNVD-\d{6}-\d{5,6}'
        info['cnnvd_ids'] = list(set(re.findall(cnnvd_pattern, content, re.IGNORECASE)))
        
        # 提取CVSS评分
        cvss_pattern = r'CVSS[:\s]+(\d+\.?\d*)'
        info['cvss_scores'] = list(set(re.findall(cvss_pattern, content, re.IGNORECASE)))
        
        # 提取风险等级
        severity_keywords = ['严重', '高危', '中危', '低危', 'Critical', 'High', 'Medium', 'Low']
        for keyword in severity_keywords:
            if keyword in content:
                info['severity_levels'].append(keyword)
        
        return info
