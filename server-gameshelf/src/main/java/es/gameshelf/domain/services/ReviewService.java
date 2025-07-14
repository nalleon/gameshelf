package es.gameshelf.domain.services;

import es.gameshelf.domain.Game;
import es.gameshelf.domain.PhotoReview;
import es.gameshelf.domain.Review;
import es.gameshelf.domain.User;
import es.gameshelf.domain.interfaces.repository.IReviewRepository;
import es.gameshelf.domain.interfaces.service.IReviewService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * @author Nabil L. A. @nalleon
 */
@Service
public class ReviewService implements IReviewService {
    /**
     * Properties
     */
    IReviewRepository repository;

    /**
     * Setter for the autowired service
     * @param repository of the service
     */
    @Autowired
    public void setRepository(IReviewRepository repository) {
        this.repository = repository;
    }


    @Override
    public Review add(String content, User user, Game game, Set<PhotoReview> photoReviewSet) {
        Review item = new Review();
        item.setContent(content);
        item.setUser(user);
        item.setGame(game);
        item.setPhotoReviewSet(photoReviewSet);
        return repository.save(item);
    }

    @Override
    public List<Review> findAll() {
        return repository.findAll();
    }

    @Override
    public List<Review> findAllByUser(User user) {
        return repository.findAllByUser(user);
    }

    @Override
    public List<Review> findAllByGame(Game game) {
        return repository.findAllByGame(game);
    }

    @Override
    public List<Review> findAllByUserLatest(User user) {
        return repository.findAllByUserLatest(user);
    }

    @Override
    public List<Review> findAllByGameLatest(Game game) {
        return repository.findAllByGameLatest(game);
    }

    @Override
    public int countAllGroupedByUser(User user) {
        return repository.countAllGroupedByUser(user);
    }

    @Override
    public int countAllGroupedByGame(Game game) {
        return repository.countAllGroupedByGame(game);
    }


    @Override
    public Review findById(Integer id) {
        return repository.findById(id);
    }

    @Override
    public boolean delete(Integer id) {
        return repository.delete(id);
    }

    @Override
    public Review update(Integer id, String content, User user, Game game, Set<PhotoReview> photoReviewSet) {
        Review item = new Review(id);
        item.setContent(content);
        item.setUser(user);
        item.setGame(game);
        item.setPhotoReviewSet(photoReviewSet);
        return repository.update(item);
    }
}
