﻿using System.Drawing;

namespace TrRebootTools.Shared.Cdc.Shadow
{
    internal class ShadowGameInfo : CdcGameInfo
    {
        public override CdcGame Game => CdcGame.Shadow;

        public override string ExeName => "SOTTR.exe";

        public override string ShortName => "SOTTR";

        public override Image Icon => Properties.Resources.Shadow;

        public override string RegistryDisplayName => "Shadow of the Tomb Raider";

        public override string ArchivePlatform => "pcx64-w";

        public override ulong LocalePlatformMask => 0;

        public override bool UsesFourccTextureFormat => false;

        public override bool UsesWwise => true;

        public override Language[] Languages { get; } = new Language[]
        {
            new(0xFFFFFFFFFFFF0400 | 1,         "en", "ENGLISH"),
            new(0xFFFFFFFFFFFF0400 | 2,         "fr", "FRENCH"),
            new(0xFFFFFFFFFFFF0400 | 4,         "de", "GERMAN"),
            new(0xFFFFFFFFFFFF0400 | 8,         "it", "ITALIAN"),
            new(0xFFFFFFFFFFFF0400 | 0x10,      "es419", "LATAMSPANISH"),
            new(0xFFFFFFFFFFFF0400 | 0x20,      "es", "IBERSPANISH"),
            new(0xFFFFFFFFFFFF0400 | 0x40,      "ja", "JAPANESE"),
            new(0xFFFFFFFFFFFF0400 | 0x80,      "pt", "PORTUGUESE"),
            new(0xFFFFFFFFFFFF0400 | 0x100,     "pl", "POLISH"),
            new(0xFFFFFFFFFFFF0400 | 0x200,     "ru", "RUSSIAN"),
            new(0xFFFFFFFFFFFF0400 | 0x400,     "nl", "DUTCH"),
            new(0xFFFFFFFFFFFF0400 | 0x800,     "ko", "KOREAN"),
            new(0xFFFFFFFFFFFF0400 | 0x1000,    "zhhant", "CHINESE"),
            new(0xFFFFFFFFFFFF0400 | 0x2000,    "zhhans", "SIMPLECHINESE"),
            new(0xFFFFFFFFFFFF0400 | 0x8000,    "ar", "ARABIC")
        };
    }
}
