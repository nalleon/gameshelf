package es.gameshelf.domain.services;

import es.gameshelf.domain.PhotoReview;
import es.gameshelf.domain.interfaces.repository.IPhotoRepository;
import es.gameshelf.domain.interfaces.service.IPhotoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class PhotoReviewService implements IPhotoService {
    /**
     * Properties
     */
    IPhotoRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IPhotoRepository repository) {
        this.repository = repository;
    }

    @Override
    public PhotoReview add(String name, String photo, String type) {
        PhotoReview item = new PhotoReview();
        item.setName(name);
        item.setType(type);
        item.setAdditionalText(photo);
        return repository.save(item);
    }

    @Override
    public List<PhotoReview> findAll() {
        return repository.findAll();
    }

    @Override
    public PhotoReview findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public PhotoReview findByName(String name) {
        return repository.findByName(name);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public PhotoReview update(Integer id, String name, String photo, String type) {
        PhotoReview item = new PhotoReview(id);
        item.setName(name);
        item.setType(type);
        item.setAdditionalText(photo);
        return repository.update(item);
    }
}
