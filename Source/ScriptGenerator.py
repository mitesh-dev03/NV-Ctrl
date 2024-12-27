import os
import subprocess
import textwrap
import xml.etree.ElementTree as ET

class ScriptGenerator:

    def __init__(self):
        self.RootPath = "./MetaScripts/"

    def Generate(self, Metascript: str, ScriptID: str, Substitutions: dict = {}) -> None:
        Document = ET.parse(f"./MetaScripts/{Metascript}.xml")
        DocRoot = Document.getroot()
        Target = DocRoot.findall(f"./script[@ID='{ScriptID}']")
        if(len(Target) != 1):
            raise Exception(f"Invalid MetaScript ID")

        Content = Target[0].find("./source").text
        if(len(Substitutions) > 0):
            Content = Content.format(**Substitutions)
        self.WriteFile(textwrap.dedent(Content),
                  Target[0].find("./path").text,
                  Target[0].find("./executable").text == "True")

    def Purge(self) -> None:
        for Dir in os.listdir(self.RootPath):
            DocObj = ET.parse(self.RootPath + Dir)
            PathList = DocObj.getroot().findall("./script/path")
            for Path in PathList:
                if(os.path.isfile(Path.text)):
                    os.remove(Path.text)
                    print(f"Removed File : {Path.text}")

    def WriteFile(self, Content, Path, IsExecutable=False) -> None:
        try:
            if not os.path.exists(os.path.dirname(Path)):
                os.makedirs(os.path.dirname(Path))
            with open(Path, mode='w', encoding='utf-8') as Target:
                Target.write(Content)
            if IsExecutable:
                subprocess.run(['chmod', '+x', Path])
            print(f"Created File : {Path}")
        except OSError as e:
            raise Exception(f"Failed to create file {Path}")