from typing import Dict, Optional, Any

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from mkdocs.config.base import Config
from mkdocs.config import config_options


class ModifyBaseURLPluginConfig(Config):
    prefix = config_options.Type(str, default='')


class ModifyBaseURLPlugin(BasePlugin[ModifyBaseURLPluginConfig]):
    def _modify_base_url(self, original: str) -> str:
        return self.config.prefix + original

    def on_page_context(
            self, context: Dict[str, Any], *, page: Page, config: MkDocsConfig, nav: Navigation
    ) -> Optional[Dict[str, Any]]:
        original_base_url = context['base_url']
        context['base_url'] = self._modify_base_url(original_base_url)
        return context

    def on_template_context(
            self, context: Dict[str, Any], *, template_name: str, config: MkDocsConfig
    ) -> Optional[Dict[str, Any]]:
        original_base_url = context['base_url']
        context['base_url'] = self._modify_base_url(original_base_url)
        return context
