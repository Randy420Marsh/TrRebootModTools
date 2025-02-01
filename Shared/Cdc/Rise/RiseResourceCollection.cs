﻿using System.IO;
using System.Runtime.InteropServices;

namespace TrRebootTools.Shared.Cdc.Rise
{
    internal class RiseResourceCollection : ResourceCollection<RiseResourceCollection.ResourceLocation, uint>
    {
        public RiseResourceCollection(ulong nameHash, ulong locale, Stream stream)
            : base(nameHash, locale, stream)
        {
        }

        public override CdcGame Game => CdcGame.Rise;

        protected override int HeaderVersion => 22;

        protected override int HeaderLocaleSize => 0;

        protected override int DependencyLocaleSize => 4;

        protected override ResourceReference MakeResourceReference(ResourceIdentification<uint> identification, ResourceLocation location)
        {
            return new ResourceReference(
                (ResourceType)location.Type,
                (ResourceSubType)identification.SubType,
                location.Id,
                0xFFFFFFFF00000000 | identification.Locale,
                location.ArchiveId,
                0,
                location.ArchivePart,
                location.OffsetInArchive,
                location.SizeInArchive,
                location.OffsetInBatch,
                identification.RefDefinitionsSize,
                identification.BodySize
            );
        }

        protected override ResourceIdentification<uint> MakeResourceIdentification(ResourceReference resourceRef)
        {
            return new ResourceIdentification<uint>
            {
                Type = (byte)resourceRef.Type,
                SubType = (int)resourceRef.SubType,
                Id = resourceRef.Id,
                Locale = 0xFFFFFFFF
            };
        }

        protected override ResourceLocation MakeResourceLocation(ResourceReference resourceRef)
        {
            return new ResourceLocation
            {
                Type = (int)resourceRef.Type,
                Id = resourceRef.Id
            };
        }

        protected override void UpdateResourceLocation(ref ResourceLocation location, ResourceReference resourceRef)
        {
            location.ArchiveId = (byte)resourceRef.ArchiveId;
            location.ArchivePart = (short)resourceRef.ArchivePart;
            location.OffsetInArchive = resourceRef.Offset;
            location.SizeInArchive = resourceRef.Length;
            location.OffsetInBatch = resourceRef.OffsetInBatch;
        }

        [StructLayout(LayoutKind.Sequential)]
        public struct ResourceLocation
        {
            public int UniqueKey;
            public int Padding;
            public short ArchivePart;
            public short ArchiveId;
            public int OffsetInArchive;
            public int SizeInArchive;
            public int OffsetInBatch;

            public int Type
            {
                get { return UniqueKey >> 24; }
                set { UniqueKey = (value << 24) | (UniqueKey & 0x00FFFFFF); }
            }

            public int Id
            {
                get { return UniqueKey & 0x00FFFFFF; }
                set { UniqueKey = (int)(UniqueKey & 0xFF000000) | value; }
            }
        }
    }
}
