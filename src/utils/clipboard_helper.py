"""
Clipboard and content copying utilities
"""

import streamlit as st
from typing import List
from datetime import datetime
import json

class ClipboardHelper:
    """Helper class for clipboard operations and content copying"""
    
    @staticmethod
    def create_copy_button_html(content: str, button_id: str, button_text: str = "📋 Copy to Clipboard") -> str:
        """
        Create HTML with JavaScript for a copy button
        
        Args:
            content: Text content to copy
            button_id: Unique ID for the button
            button_text: Text to display on button
            
        Returns:
            HTML string with copy functionality
        """
        # Escape content for JavaScript
        escaped_content = ClipboardHelper._escape_for_javascript(content)
        
        return f"""
        <div style="margin: 10px 0;">
            <button 
                onclick="copyToClipboard_{button_id}()" 
                style="
                    background-color: #0066cc;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 14px;
                    font-weight: bold;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    transition: background-color 0.3s;
                "
                onmouseover="this.style.backgroundColor='#0052a3'"
                onmouseout="this.style.backgroundColor='#0066cc'"
            >
                {button_text}
            </button>
            <span id="copyStatus_{button_id}" style="margin-left: 10px; color: green; font-size: 12px; font-weight: bold;"></span>
        </div>
        
        <script>
        function copyToClipboard_{button_id}() {{
            const text = "{escaped_content}";
            
            if (navigator.clipboard && window.isSecureContext) {{
                // Modern clipboard API
                navigator.clipboard.writeText(text).then(function() {{
                    document.getElementById('copyStatus_{button_id}').innerText = '✅ Copied successfully!';
                    setTimeout(() => {{
                        document.getElementById('copyStatus_{button_id}').innerText = '';
                    }}, 3000);
                }}).catch(function(err) {{
                    console.error('Could not copy text: ', err);
                    fallbackCopy_{button_id}(text);
                }});
            }} else {{
                fallbackCopy_{button_id}(text);
            }}
        }}
        
        function fallbackCopy_{button_id}(text) {{
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            try {{
                const successful = document.execCommand('copy');
                if (successful) {{
                    document.getElementById('copyStatus_{button_id}').innerText = '✅ Copied successfully!';
                }} else {{
                    document.getElementById('copyStatus_{button_id}').innerText = '⚠️ Copy may have failed - check manual method';
                }}
                setTimeout(() => {{
                    document.getElementById('copyStatus_{button_id}').innerText = '';
                }}, 3000);
            }} catch (err) {{
                console.error('Fallback copy failed: ', err);
                document.getElementById('copyStatus_{button_id}').innerText = '❌ Copy failed - use manual method';
                setTimeout(() => {{
                    document.getElementById('copyStatus_{button_id}').innerText = '';
                }}, 3000);
            }}
            
            document.body.removeChild(textArea);
        }}
        </script>
        """
    
    @staticmethod
    def _escape_for_javascript(text: str) -> str:
        """
        Escape text for safe inclusion in JavaScript
        
        Args:
            text: Text to escape
            
        Returns:
            Escaped text safe for JavaScript
        """
        return (text
                .replace('\\', '\\\\')
                .replace('"', '\\"')
                .replace("'", "\\'")
                .replace('\n', '\\n')
                .replace('\r', '')
                .replace('\t', '\\t')
                .replace('`', '\\`')
                .replace('${', '\\${'))
    
    @staticmethod
    def render_copy_methods(content: str, index: int, title: str = "Copy Content"):
        """
        Render multiple copy methods for content
        
        Args:
            content: Content to copy
            index: Unique index for this content
            title: Title for the copy section
        """
        st.markdown(f"**📋 {title}:**")
        
        # Method 1: JavaScript copy button
        copy_html = ClipboardHelper.create_copy_button_html(
            content=content,
            button_id=f"content_{index}",
            button_text="📋 Copy to Clipboard"
        )
        st.components.v1.html(copy_html, height=80)
        
        # Method 2: Manual selection area
        st.text_area(
            "Manual Copy (Triple-click to select all):",
            value=content,
            height=120,
            key=f"manual_copy_{index}_{hash(content) % 10000}",
            help="Triple-click to select all text, then Ctrl+C (Windows) or Cmd+C (Mac) to copy"
        )
    
    @staticmethod
    def create_bulk_copy_functionality(contents: List[str], labels: List[str] = None):
        """
        Create bulk copy functionality for multiple contents
        
        Args:
            contents: List of content strings
            labels: Optional labels for each content
        """
        if not contents:
            return
        
        if labels is None:
            labels = [f"Content {i+1}" for i in range(len(contents))]
        
        # Individual copy buttons
        for i, (content, label) in enumerate(zip(contents, labels)):
            with st.expander(f"📋 {label}", expanded=False):
                ClipboardHelper.render_copy_methods(content, i, f"Copy {label}")
        
        # Bulk operations
        st.markdown("---")
        st.markdown("**📚 Bulk Operations:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Copy all as separate items
            all_separate = "\n\n" + "="*50 + "\n\n".join([
                f"{label.upper()}:\n\n{content}"
                for label, content in zip(labels, contents)
            ])
            
            st.download_button(
                label="💾 Download All Separate",
                data=all_separate,
                file_name=f"all_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                help="Download all content in separate sections"
            )
        
        with col2:
            # Copy all as JSON
            json_data = {
                label: content for label, content in zip(labels, contents)
            }
            
            st.download_button(
                label="📄 Download as JSON",
                data=json.dumps(json_data, indent=2),
                file_name=f"content_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                help="Download all content as structured JSON"
            )
        
        with col3:
            # Copy all concatenated
            all_concatenated = "\n\n".join(contents)
            
            st.download_button(
                label="📝 Download Concatenated",
                data=all_concatenated,
                file_name=f"concatenated_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                help="Download all content concatenated together"
            )
    
    @staticmethod
    def render_copy_instructions():
        """Render instructions for copying content"""
        with st.expander("📖 Copy Instructions", expanded=False):
            st.markdown("""
            ### How to Copy Content:
            
            **Method 1: One-Click Copy Button**
            - Click the blue "📋 Copy to Clipboard" button
            - Look for the green "✅ Copied successfully!" message
            - Paste anywhere using Ctrl+V (Windows) or Cmd+V (Mac)
            
            **Method 2: Manual Selection**
            - Triple-click in the text area to select all text
            - Press Ctrl+C (Windows) or Cmd+V (Mac) to copy
            - Paste anywhere using Ctrl+V (Windows) or Cmd+V (Mac)
            
            **Method 3: Download Files**
            - Use download buttons to save content as text files
            - Open the files in any text editor
            - Copy from there to your preferred platform
            
            **Troubleshooting:**
            - If copy button doesn't work, your browser may not support clipboard API
            - Use the manual selection method as fallback
            - Download option always works as a backup
            - Make sure you're on a secure connection (HTTPS) for best copy support
            """)
