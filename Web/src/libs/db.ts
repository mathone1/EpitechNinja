import Dexie, { type Table } from 'dexie';

export interface DBProgress {
    id: number
    userId: number
    progress: number
    synced: boolean
}

export interface DBUser {
    id: number
    userId: number
}

export class SubClassedDexie extends Dexie {

    progress!: Table<DBProgress>;
    currentUser!: Table<DBUser>;

    constructor() {
        super('database');
        this.version(1).stores({
            progress: 'id, userId, progress, synced',
            currentUser: 'id, userId'
        });
    }

}

export const db = new SubClassedDexie();
