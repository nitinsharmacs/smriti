import { type UploadTxnType } from 'src/components/MediaUploader/types';
import { doNothing } from 'src/helpers';
import UploadTransaction, { type FileType } from 'src/models/UploadTransaction';
import UploadService from 'src/services/UploadService';

type FileEntries = {
  [key: string]: File;
};

type TransactionEntries = {
  [key: string]: {
    transaction: UploadTransaction;
    files: FileEntries;
    stopper: () => void;
  };
};

class UploadController {
  private uploadService: UploadService;

  private txnEntries: TransactionEntries;

  constructor(uploadService: UploadService) {
    this.txnEntries = {};
    this.uploadService = uploadService;
  }

  newUpload(
    files: FileList,
    onProgress: () => void = doNothing,
    onComplete: () => void = doNothing
  ): string {
    const txnId = this.uploadService.createTransaction();
    const mediaIds = this.uploadService.getTxnMediaIds(txnId);

    const txnFiles: FileEntries = {};
    const mediaFiles: FileType[] = [];

    [...files].forEach((file, index) => {
      mediaFiles.push({
        id: mediaIds[index],
        name: file.name,
        type: file.type,
      });

      txnFiles[mediaIds[index]] = file;
    });

    const txn = new UploadTransaction(txnId, mediaFiles);

    const stopper = this.uploadService.uploadFiles(
      txnId,
      files,
      (progresses) => {
        txn.updateMediaProgresses(progresses);
        onProgress();
      },
      () => {
        txn.complete();
        onComplete();
      }
    );

    this.txnEntries[txnId] = {
      transaction: txn,
      files: txnFiles,
      stopper,
    };

    return txnId;
  }

  stopUpload(txnId: string): boolean {
    const entry = this.txnEntries[txnId];

    if (entry) {
      this.txnEntries[txnId].transaction.stop();
      this.txnEntries[txnId].stopper();
      return true;
    }

    return false;
  }

  completeTxnPartially(txnId: string): boolean {
    const entry = this.txnEntries[txnId];

    if (!entry) return false;

    const txn = entry.transaction;

    if (!txn.anyFileUploaded()) {
      this.removeTransaction(txnId);
      return false;
    }

    txn.completePartially();
    return true;
  }

  removeTransaction(txnId: string): boolean {
    return delete this.txnEntries[txnId];
  }

  hasTransaction(txnId: string): boolean {
    return txnId in this.txnEntries;
  }

  getFailedTxnMediaFiles(txnId: string): FileList {
    const txnEntry = this.txnEntries[txnId];

    const dataTransfer = new DataTransfer();

    if (!txnEntry) return dataTransfer.files;

    const failedMediaIds: string[] = txnEntry.transaction.getFailedMediaIds();

    failedMediaIds.forEach((id) => dataTransfer.items.add(txnEntry.files[id]));

    return dataTransfer.files;
  }

  getTransactions(): UploadTxnType[] {
    return Object.values(this.txnEntries).map((entry) =>
      entry.transaction.getObject()
    );
  }
}

export default UploadController;
