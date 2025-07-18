import { useCallback, useState } from 'react';

import Button from 'src/components/Button/Button';
import Modal from 'src/components/MediaUploader/Modal/Modal';
import CollapsableMediaItems from 'src/components/MediaUploader/CollapsableMediaItems/CollapsableMediaItems';

import './retrymodal.css';

const RetryModal = () => {
  const [showMore, setShowMore] = useState<boolean>(false);

  const showMoreHandler = useCallback(() => {
    setShowMore((prev) => !prev);
  }, []);

  return (
    <Modal>
      <div className='retry-modal'>
        <h4 className='retry-modal-heading'>4 unfinished upload</h4>
        <div className='retry-controls'>
          <Button variant='contained'>Retry</Button>
          <Button
            variant='text'
            onClick={showMoreHandler}
            style={{ marginLeft: '0.5em' }}
          >
            Show more
          </Button>
        </div>
        <CollapsableMediaItems open={showMore} />
      </div>
    </Modal>
  );
};

export default RetryModal;
