export type TarEntryType = 'block-device' | 'character-device' | 'contiguous-file' | 'directory' | 'fifo' | 'file' | 'link' | 'symlink';
export interface TarHeader {
    devmajor: number | null;
    devminor: number | null;
    gid: number | null;
    gname: string;
    linkname: string | null;
    mode: number | null;
    mtime: Date | null;
    name: string;
    size: number | null;
    type: TarEntryType | null;
    uid: number | null;
    uname: string;
}
export declare function decode(buf: Uint8Array, filenameEncoding: BufferEncoding, allowUnknownFormat: boolean): TarHeader | null;
//# sourceMappingURL=headers.d.ts.map