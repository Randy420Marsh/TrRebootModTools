﻿using System.IO;
using System.Runtime.InteropServices;
using TrRebootTools.Shared.Util;

namespace TrRebootTools.Shared.Cdc.Tr2013
{
    internal class Tr2013Archive : Archive
    {
        public Tr2013Archive(string baseFilePath, ArchiveMetaData metaData)
            : base(baseFilePath, metaData)
        {
        }

        protected override CdcGame Game => CdcGame.Tr2013;
        protected override int HeaderVersion => 3;
        protected override bool SupportsSubId => false;
        protected override int ContentAlignment => 0x800;

        protected override ArchiveFileReference ReadFileReference(BinaryReader reader)
        {
            var entry = reader.ReadStruct<ArchiveFileEntry>();
            return new ArchiveFileReference(
                entry.NameHash,
                0xFFFFFFFF00000000 | entry.Locale,
                (entry.PackedOffset >> 4) & 0x7F,
                0,
                entry.PackedOffset & 0xF,
                (int)(entry.PackedOffset & 0xFFFFF800),
                entry.Size
            );
        }

        protected override void WriteFileReference(BinaryWriter writer, ArchiveFileReference fileRef)
        {
            var entry =
                new ArchiveFileEntry
                {
                    NameHash = (uint)fileRef.NameHash,
                    Locale = (uint)fileRef.Locale,
                    Size = fileRef.Length,
                    PackedOffset = fileRef.Offset | (fileRef.ArchiveId << 4) | fileRef.ArchivePart
                };
            writer.WriteStruct(entry);
        }

        [StructLayout(LayoutKind.Sequential)]
        protected struct ArchiveFileEntry
        {
            public uint NameHash;
            public uint Locale;
            public int Size;
            public int PackedOffset;
        }
    }
}
